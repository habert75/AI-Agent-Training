import requests
import os
from pprint import pprint

headers = {
    "Content-Type": "application/json",
}

response = requests.get(
    "https://6k9mzlo595m66s-8080.proxy.runpod.net/v1/models",
    headers=headers,
)

print("--- Full response: ---")
print(response)
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["message"]["content"])
