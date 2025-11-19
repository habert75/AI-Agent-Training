import os
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key=os.environ.get("GROK_API_KEY"),
)

response = client.chat.completions.create(
    model="grok-3-mini",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {
            "role": "user",
            "content": "Tell me a joke.",
        },
    ],
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
