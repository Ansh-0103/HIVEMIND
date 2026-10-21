import os # to read api keys from .env file
from concurrent.futures import ThreadPoolExecutor # to ask  question to gemini and  groq in same time
from dotenv import load_dotenv # to open env and read api keys
from google import genai # to ask question to gemini
from groq import Groq # to ask question to groq

load_dotenv()

GEMINI_MODEL = "gemini-3.8-flash"
GROQ_MODEL = "openai/gpt-oss-120b"


def ask_gemini(question):
    import time # for time.sleep() function to wait for 3 seconds before retrying a failed request to the model
    for attempt in range(3):   #three attempts to ask the model in case of failure
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) #create gemini connection
            r = client.models.generate_content(model=GEMINI_MODEL, contents=question)#hold the reply
            return r.text #return the reply text
        except Exception as e:
            msg = str(e) #turn the error message as string
            if ("503" in msg or "UNAVAILABLE" in msg) and attempt < 2:
                time.sleep(3) #wait for 3 seconds before retrying a failed request to the model
                continue
            return "Model unavailable: " + msg[:120] #return the error message if the model is unavailable
#gemini with attempts because it was  seen busy sometimes
def ask_groq(question):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=20) #create groq connection and safeguard the connection with a timeout of 20 seconds  
        r = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": question}], #the foramt of the question to be asked to the model
        )
        return r.choices[0].message.content #where the model's answer is stored and returned to the user
    except Exception as e:
        return "Model unavailable: " + str(e)[:120]
#we didn't use the reply use for groq becasue it was seen busy

MODELS = {"gemini": ask_gemini, "groq": ask_groq} #no brackets after the model names because we are not calling the function yet, we are just storing the function in a dictionary


def make_verdict(question, answers):# n=name of model(gemini or groq), a=answer from the model
    good = {n: a for n, a in answers.items() if not a.startswith("Model unavailable")} #go through the answers and filter out the ones that are unavailable
    if len(good) < 2:#if there are less than 2 answers, return a message to the user
        return "Select two or more working AIs to get a combined verdict."
    text = "\n\n".join(n.upper() + " said:\n" + a for n, a in good.items()) #join model said and its answer
    prompt = (
        "A user asked: " + question + "\n\nSeveral AIs answered:\n\n" + text +   #prompt to be sent to the model to get a combined verdict
        "\n\nWrite three short parts: 1) Where they agree, 2) Where they differ, "
        "3) A final recommendation. Keep the whole verdict under 150 words.")
    return ask_groq(prompt) #send prompt to groq

def make_hive_answer(question, answers): #here we are asking hive to make its own answer based on the answers from the models
    good = {n: a for n, a in answers.items() if not a.startswith("Model unavailable")}
    if len(good) < 2:
        return ""
    text = "\n\n".join(n.upper() + " said:\n" + a for n, a in good.items())
    prompt = ("A user asked: " + question + "\n\nSeveral AIs answered:\n\n" + text +
              "\n\nNow write ONE single best answer to the user's question yourself, "
              "combining the strongest parts of the answers above. Do not mention the AIs. "
              "Follow the user's request exactly, such as the number of lines or words.")
    return ask_groq(prompt)

'''#make_votes function is used to ask the model to judge which answer helps the user best (clarity, accuracy, usefulness) and 
give each answer a percentage so the total is 100. 
It returns a dictionary with the model names as keys and their corresponding scores as values.'''
def make_votes(question, answers): 
    import json, re 
    good = {n: a for n, a in answers.items() if not a.startswith("Model unavailable")}
    if len(good) < 2:
        return {}
    letters = {n: chr(65 + i) for i, n in enumerate(good)}
    text = "\n\n".join("ANSWER " + letters[n] + ":\n" + a for n, a in good.items())
    keys = ", ".join(letters.values())
    prompt = ("A user asked: " + question + "\n\n" + text +
              "\n\nJudge which answer helps the user best (clarity, accuracy, usefulness). "
              "Give each answer a percentage so the total is 100. "
              "Reply with ONLY a JSON object using exactly these keys: " + keys +
              '. Example: {"A": 60, "B": 40}')
    try:
        raw = ask_groq(prompt)
        data = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))#AI replies in text,I pull out the JSON part and convert it into a dictionary to get the pie chart num.
        scores = {n: float(data[letters[n]]) for n in good}#to add up the scores and convert them into percentages. 
        total = sum(scores.values())
        if total <= 0:
            return {}
        return {n: round(v * 100 / total) for n, v in scores.items()} 
    except Exception:
        return {}


    
def ask_council(question, selected=None):
    names = selected or list(MODELS) #use user's chosen AI or whole council
    short_q = question + "\n\n(Keep your answer under 100 words unless the user asked for a specific length.)"
    with ThreadPoolExecutor() as pool:
        futures = {n: pool.submit(MODELS[n], short_q) for n in names}
        model_answers = {n: f.result() for n, f in futures.items()}
    answers = dict(model_answers)
    with ThreadPoolExecutor() as pool:
        f_final = pool.submit(make_verdict, question, model_answers)
        f_hive = pool.submit(make_hive_answer, question, model_answers)
        f_votes = pool.submit(make_votes, question, model_answers)
        answers["final"] = f_final.result()
        answers["hive"] = f_hive.result()
        answers["votes"] = f_votes.result()
    return answers
import json

def saved_questions():#here saved questions are stored
    try:
        with open("backup.json", encoding="utf-8") as f:#use the backup.json file to store the saved questions and answers
            return list(json.load(f).keys()) #list of saved questions is returned to the user
    except Exception:
        return []

def ask_offline(question):
    with open("backup.json", encoding="utf-8") as f:
        return json.load(f)[question]



if __name__ == "__main__":#use this to test the code in the backend.py file
    result = ask_council(
        "only name of top 5 cricketers without any single details"
    )
    for name, text in result.items():
        print("---", name.upper(), "---")
        print(text)