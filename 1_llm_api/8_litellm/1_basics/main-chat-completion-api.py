import os
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LITELLM_API_KEY", "dummy-key"),
    base_url=os.getenv("LITELLM_BASE_URL", "http://0.0.0.0:4000"),
)

response = client.chat.completions.create(
    model="anthropic-claude-sonnet-4",
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
