# 🏥 Medical Report Summarizer GUI (VS Code / Tkinter)

import os, fitz, shutil, pdfplumber, io, re
from PIL import Image, ImageTk
import google.generativeai as genai
from openai import OpenAI
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import pandas as pd
import shutil
# 🔑 API Keys
import os

# Load the .env file
load_dotenv()

# Get keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# For testing (don’t show full keys)
print("Google Key:", GOOGLE_API_KEY[:5] + "*****")
print("DeepSeek Key:", DEEPSEEK_API_KEY[:5] + "*****")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Create OpenAI client for DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://openrouter.ai/api/v1")



# Images folder
images_folder = "images"
if os.path.exists(images_folder):
    try:
        shutil.rmtree(images_folder)
    except PermissionError:
        print("Warning: Cannot delete 'images' folder, it may be in use.")

os.makedirs(images_folder, exist_ok=True)

# ------------------------------
# Extraction functions
# ------------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        pix.save(f"images/page_{i+1}.png")
        text += page.get_text("text")
    doc.close()
    return text.strip()

def extract_text_from_image(img_path):
    from pytesseract import image_to_string
    return image_to_string(Image.open(img_path), lang="eng+hin").strip()

def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)
    return tables

def chunk_text(text, max_chars=5000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# ------------------------------
# AI functions
# ------------------------------
def generate_summary_with_gemini(text, mode="normal", language="en"):
    prompt_template = f"""
You are a friendly Indian medical assistant.
Language: {"Hindi" if language=="hi" else "English"}
Mode: {"Explain Like I am 5" if mode=="eli5" else "Normal summary"}

🧍 PATIENT DETAILS
• Name: __
• Age: __
• Date: __
• Gender: __
• State: __
• Country: India
• Phone Number: __

🏥 MEDICAL INSIGHTS
• Disease Name: __
• Common symptoms: __
• Likely cause: __
• Risk level (Low/Medium/High): __
• Possible medicines prescribed: __
• Side effects to watch for: __
• How to avoid it in future (Indian context): __
• What you should ask your doctor next time: __
• Extra care to take now: __

🥗 DIET & LIFESTYLE RECOMMENDATIONS
• Eat more: __
• Avoid eating: __
• Good drinks: __
• Avoid drinks: __

👨‍⚕️ DOCTOR'S NOTE
• One-liner advice: __

📊 STATISTICS (India-specific)
• Recent yearly trend in India: __
• Most affected states: __

Report:
{text}
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chunks = chunk_text(text)
        final_summary = ""
        for idx, chunk in enumerate(chunks, start=1):
            response = model.generate_content(prompt_template.replace("{text}", chunk))
            final_summary += f"\n--- CHUNK {idx} SUMMARY ---\n" + response.text.strip()
        return final_summary.strip()
    except Exception as e:
        return f"❌ Gemini error: {e}"

def validate_with_gpt(summary):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Cross-check the medical summary for correctness."},
                {"role": "user", "content": summary}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ GPT validation error: {e}"

def extract_disease_name(summary_text):
    match = re.search(r"• Disease Name:\s*(.+)", summary_text)
    if match:
        disease = match.group(1).strip()
        if disease and disease != "__":
            return disease
    return None

def generate_dynamic_disease_charts(summary_text):
    disease_name = extract_disease_name(summary_text) or "Unknown"
    if disease_name == "Unknown":
        print("⚠️ No disease name found. Skipping charts.")
        return
    states = ["Delhi", "UP", "Bihar", "Maharashtra", "Kerala"]
    cases = [120, 340, 220, 410, 150]
    plt.figure(figsize=(8,5))
    plt.bar(states, cases, color="#4CAF50")
    plt.title(f"{disease_name} Cases in India (Simulated Data)")
    plt.xlabel("States")
    plt.ylabel("Cases")
    plt.show()
