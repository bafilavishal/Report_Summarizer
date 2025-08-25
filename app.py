from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
# Import your existing medical summarizer functions
from summarizer_utils import (
    extract_text_from_pdf,
    extract_text_from_image,
    generate_summary_with_gemini,
    validate_with_gpt,
    generate_dynamic_disease_charts
)

UPLOAD_FOLDER = "uploads"
SUMMARY_FOLDER = "summaries"
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'mp3', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        language = request.form.get("language", "en")
        mode = request.form.get("mode", "normal")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text based on file type
            if filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif filename.lower().endswith((".jpg", ".jpeg", ".png")):
                text = extract_text_from_image(file_path)
            else:
                text = ""

            if text:
                # Generate summary
                summary = generate_summary_with_gemini(text, mode=mode, language=language)

                # Validate with GPT
                try:
                    validated = validate_with_gpt(summary)
                except Exception as e:
                    validated = summary + f"\n\n⚠️ GPT validation error: {e}"

                # Save validated summary
                summary_file = os.path.join(SUMMARY_FOLDER, filename + "_summary.txt")
                with open(summary_file, "w", encoding="utf-8") as f:
                    f.write(validated)

                # Generate charts if disease name is present
                try:
                    generate_dynamic_disease_charts(validated)
                except Exception as e:
                    print(f"⚠️ Skipping charts: {e}")

                # 👉 Render result.html instead of index.html
                return render_template("result.html", summary=validated, summary_file=summary_file)

            else:
                error = "❌ No text found in the uploaded file."
                return render_template("result.html", error=error)
        else:
            error = "❌ Invalid file type. Allowed: PDF, JPG, PNG, MP3, WAV."
            return render_template("result.html", error=error)

    # GET request → just show upload form
    return render_template("index.html")

@app.route("/download/<path:filename>")
def download_file(filename):
    safe_path = os.path.join(SUMMARY_FOLDER, os.path.basename(filename))
    if os.path.exists(safe_path):
        return send_file(safe_path, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

