import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

GEMINI_MODEL = "gemini-3.8-flash"
GROQ_MODEL = "openai/gpt-oss-120b"


def ask_gemini(question):
    import time
    for attempt in range(3):
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            r = client.models.generate_content(model=GEMINI_MODEL, contents=question)
            return r.text
        except Exception as e:
            msg = str(e)
            if ("503" in msg or "UNAVAILABLE" in msg) and attempt < 2:
                time.sleep(3)
                continue
            return "Model unavailable: " + msg[:120]

def ask_groq(question):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=20)
        r = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": question}],
        )
        return r.choices[0].message.content
    except Exception as e:
        return "Model unavailable: " + str(e)[:120]


MODELS = {"gemini": ask_gemini, "groq": ask_groq}


def make_verdict(question, answers):
    good = {n: a for n, a in answers.items() if not a.startswith("Model unavailable")}
    if len(good) < 2:
        return "Select two or more working AIs to get a combined verdict."
    text = "\n\n".join(n.upper() + " said:\n" + a for n, a in good.items())
    prompt = (
        "A user asked: " + question + "\n\nSeveral AIs answered:\n\n" + text +
        "\n\nWrite three short parts: 1) Where they agree, 2) Where they differ, "
        "3) A final recommendation. Keep the whole verdict under 150 words.")
    return ask_groq(prompt)


def ask_council(question, selected=None):
    names = selected or list(MODELS)
    short_q = question + "\n\n(Keep your answer under 120 words.)"
    with ThreadPoolExecutor() as pool:
        futures = {n: pool.submit(MODELS[n], short_q) for n in names}
        answers = {n: f.result() for n, f in futures.items()}
    answers["final"] = make_verdict(question, answers)
    return answers
import json

def saved_questions():
    try:
        with open("backup.json", encoding="utf-8") as f:
            return list(json.load(f).keys())
    except Exception:
        return []

def ask_offline(question):
    with open("backup.json", encoding="utf-8") as f:
        return json.load(f)[question]



if __name__ == "__main__":
    result = ask_council(
        "only name of top 5 cricketers without any single details"
    )
    for name, text in result.items():
        print("---", name.upper(), "---")
        print(text)