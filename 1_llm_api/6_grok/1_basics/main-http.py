import requests
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROK_API_KEY")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

data = {
    "model": "grok-3-mini",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
}

response = requests.post(
    "https://api.x.ai/v1/chat/completions", headers=headers, json=data
)

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["message"]["content"])
