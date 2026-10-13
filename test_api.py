import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

try:
    g = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    r = g.models.generate_content(model="gemini-3.8-flash", contents="Say hello in one line")
    print("GEMINI:", r.text)
except Exception as e:
    print("Gemini error:", str(e)[:200])

try:
    q = Groq(api_key=os.getenv("GROQ_API_KEY"))
    r = q.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": "Say hello in one line"}],
    )
    print("GROQ:", r.choices[0].message.content)
except Exception as e:
    print("Groq error:", str(e)[:200])