# HIVE MIND

**One question. A hive of AIs. One smarter answer.**

## What is Hive Mind?

Hive Mind is a multi-AI chatbot. You type one question, and it is sent to several AI models at the same time. Each AI's answer is shown in its own card. Then the Hive reads all the answers and gives you one combined result: a verdict, a single best answer, and a chart showing which answer it favours.

## The problem with using a single AI

- Different AIs give different answers to the same question, and you cannot tell which one is right.
- A single AI can make mistakes or sound confident when it is wrong, and nothing is there to check it.
- To compare AIs, you have to open many websites, type the same question again and again, and compare the answers yourself.
- If that one AI is slow, busy or has reached its limit, you are stuck.

## How Hive Mind solves it

Hive Mind asks several AIs at once and puts their answers side by side. It then compares them for you, so you can see where they agree, where they differ, and what the best final answer is. If one AI fails, the others still work, and an offline mode with saved answers keeps the demo running even without internet.

## Features

- Three modes: Single AI, Full Council (all AIs) and Custom Mix (pick your own)
- All AIs answer in parallel
- One card per AI, so answers are easy to compare
- A combined Hive Verdict, a single Hive answer and a Hive's Pie chart
- If one AI fails, the rest still work
- Answers are short and precise

## Terminologies used
>>>Voices of the Hive: The separate answers from each AI, one card each 
>>>Hive Verdict:  A short summary of where the AIs agree, where they differ, and a final recommendation
>>>Hive's Pick : A pie chart showing how strongly the Hive favours each answer
>>>Full Council : Mode where every AI answers and the Hive merges them

## Tech used

- Python 3.12
- Streamlit for the web interface
- Google Gemini API and Groq API (GPT-OSS model), both on free tiers
- python-dotenv to keep API keys private
- Parallel calls using ThreadPoolExecutor
- Altair for the pie chart

## Project files

***File :What it does ?
| `app.py` | The Streamlit page
| `backend.py` | Calls the AIs and builds the Hive's verdict, answer and scores 
| `make_backup.py` | Saves real answers into `backup.json` for offline mode 
| `backup.json` | Saved answers used by offline demo mode 
| `requirements.txt` | List of libraries to install 
| `.env.example` | Template for the API keys |

## Future scope()
>>>THE HIVEMIND do not have any limitations,the given below are the features that can improvise it to become a platform of larger service

>>>More AI models: add ChatGPT, Claude and others with one small function each, so the Hive becomes a bigger council.
>>>Paid API plans: move from free tiers to paid ones, so many users can ask at the same time without hitting limits.
>>>Accounts and history:  let users sign in, save their past questions and compare how the Hive's answers change.
>>>A database and caching: store popular questions and answers, which saves time and API cost.
>>>Subject-specific councils: for example, a council for health information, law or education that uses the models best suited to each field.
>>>Real voting: let users vote on the best answer, and use those votes to improve the Hive's scoring.

## Authors

**Ansh Shukla**
BCA (Data Science and AI), BBDU Lucknow

## Project partner

**Ravi Kumar Raj**
BCA (Data Science and AI), BBDU Lucknow