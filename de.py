from openai import OpenAI
import os

# Replace with your real key or use environment variable
os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, test if my API key works!"}]
    )
    print("✅ API key works! Response:")
    print(response.choices[0].message.content)
except Exception as e:
    print("❌ API key failed:", e)
