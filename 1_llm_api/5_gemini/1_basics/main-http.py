import requests
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

headers = {
    "Content-Type": "application/json",
}

data = {"contents": [{"parts": [{"text": "Tell me a joke."}]}]}

response = requests.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
    headers=headers,
    json=data,
)

print("--- Full response: ---")
pprint(response.json())
