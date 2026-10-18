import json
from backend import ask_council

QUESTIONS = [
    "Describe what is multi llm model in 100 woreds?",
    "What is the formula for calculating simple interest?",
    "write a 10-12 lines poem about the beauty of nature",
    "write a program to obtain factorial of a number",
    "which is the greatest Christopher Nolan movie ever made in 100 words?",
]

backup = {}
for q in QUESTIONS:
    print("Asking:", q)
    backup[q] = ask_council(q)

with open("backup.json", "w", encoding="utf-8") as f:
    json.dump(backup, f, ensure_ascii=False, indent=2)

print("Saved backup.json")