import os, time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://integrate.api.nvidia.com/v1",
                api_key=os.getenv("NVIDIA_API_KEY"), timeout=120, max_retries=0)
start = time.time()
try:
    r = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning-30b-a3b",
        messages=[{"role": "user", "content": "Say hi in one line"}])
    print(repr(r.choices[0].message.content))
except Exception as e:
    print("ERROR:", str(e)[:200])
print("seconds:", round(time.time() - start, 1))