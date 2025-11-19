import requests
import os
from pprint import pprint

headers = {
    "Content-Type": "application/json",
}

data = {
    "model": "lukaskellerstein/tools-mistral-16bit-merged-new",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
}

# VLLM
response = requests.post(
    "https://glk7vf0qt47hw5-8080.proxy.runpod.net/v1/chat/completions",
    headers=headers,
    json=data,
)

print("--- Full response: ---")
print(response)
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["message"]["content"])
