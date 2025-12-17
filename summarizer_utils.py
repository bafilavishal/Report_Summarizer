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
import google.generativeai as genai
from openai import OpenAI

# ✅ Directly set your keys here (not secure, but no .env needed)
GOOGLE_API_KEY = "AIzaSyDrVsMVmWc-Sl4nXlkyu_WYCF-X3dekc1Y"   # replace with your real key
DEEPSEEK_API_KEY = "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" # replace with your real key


# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Create OpenAI client for DeepSeek
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

def generate_summary_with_openrouter(text, mode="normal", language="en"):
    prompt_template = """
        You are a medical summarizer AI.

STRICT RULES:
- Do NOT review, analyze, or critique the report.
- Do NOT say "the summary provided" or "points to consider".
- Do NOT explain, comment, or suggest improvements.
- ONLY fill in the template fields below.
- EVERY field under 🩺 Medical Insights MUST be filled.
- If the report does not explicitly provide information for a field, infer a reasonable value based on context.
- Use **very simple language** that anyone can understand; avoid medical or technical terms.
-Use very simple words. Short sentences. Explain any medical term in everyday words.
-Use a friendly, reassuring tone. Encourage the patient to follow healthy habits.
-Focus on what the patient can do to improve their health. Give clear, practical advice.
-Convert lab results and medical measurements into simple explanations that anyone can understand.

-give a little descriptive information.
- Output ONLY the template, nothing else.
- No introductions, no extra sentences before or after.
- Output MUST begin with "🧾 Medical Report Summary".
- Fill the patient details from the report; use "__" only if the information is completely missing.


TEMPLATE TO FILL:
🧾 Medical Report Summary

👤 Patient Details:
- Name: __
- Age: __
- Gender: __
- Occupation: __
- State: __
- Country: __
- Phone: __

🩺 Medical Insights:
- Disease Name: __
- Common Symptoms: __
- Likely Cause: __
- Risk Level: __
- Possible Medicines Prescribed: __
- Side Effects: __
- Future Prevention: __

🥗 Diet & Lifestyle Recommendations:
- Eat: __
- Drink: __
- Avoid: __

📊 Statistics:


📌 Doctor’s Note:
__
    Report:
    {text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ Valid OpenRouter model
            messages=[
                {"role": "system", "content": "You are a helpful medical summarizer."},
                {"role": "user", "content": prompt_template.replace("{text}", text)}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ OpenRouter error: {e}"


# ✅ Gemini for real-time graphs / trends
def generate_dynamic_disease_charts(summary_text):
    disease_name = extract_disease_name(summary_text) or "Unknown"
    if disease_name == "Unknown":
        print("⚠️ No disease name found. Skipping charts.")
        return

    try:
        # Use Gemini to simulate trend data (instead of hardcoding)
        model = genai.GenerativeModel("gemini-1.5-flash")
        trend_prompt = f"""
Provide a short JSON dataset showing approximate {disease_name} case counts 
in 5 Indian states for visualization. 
Format strictly as: {{"states": [...], "cases": [...]}} with 5 values each.
"""
        response = model.generate_content(trend_prompt)
        data = eval(response.text.strip())  # Convert Gemini’s JSON-like output

        states = data.get("states", ["Delhi","UP","Bihar","Maharashtra","Kerala"])
        cases = data.get("cases", [120,340,220,410,150])

        plt.figure(figsize=(8,5))
        plt.bar(states, cases, color="#4CAF50")
        plt.title(f"{disease_name} Cases in India (Gemini Real-time Data)")
        plt.xlabel("States")
        plt.ylabel("Cases")
        plt.show()

    except Exception as e:
        print(f"⚠️ Gemini chart error: {e}")


#  latest 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta

bcrypt = Bcrypt()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.check_password_hash(hashed, password)

def generate_token(user_id):
    return create_access_token(identity=str(user_id), expires_delta=timedelta(days=7))
