import os # to read api keys from .env file
import ThreadPoolExecutor# to ask  question to gemini and  groq in same time
import load_dotenv # to open env and read api keys
import genai # to ask question to gemini
import Groq # to ask question to groq
import time #brings up the  time.sleep() function to wait for 3 seconds before retrying a failed request to the model
import json
'''JSON is a plain-text format for storing data in a structured way.
    It looks almost the same as a Python dictionary:
    {"A": 60, "B": 40}
    json.loads(...) is the converter: it turns the text into a real Python dictionary.
    '''
import re
'''re stands for regular expressions, a way to search for a pattern inside text.'''
