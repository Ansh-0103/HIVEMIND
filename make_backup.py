import json
from backend import ask_council

QUESTIONS = [
    "Describe BBDU lucknow in 100 words",
    "How ai can help in education in 100 words?",
    "describe api in 100 words in 100 words",
]

backup = {}
for q in QUESTIONS:
    print("Asking:", q)
    backup[q] = ask_council(q)

with open("backup.json", "w", encoding="utf-8") as f:
    json.dump(backup, f, ensure_ascii=False, indent=2)

print("Saved backup.json")