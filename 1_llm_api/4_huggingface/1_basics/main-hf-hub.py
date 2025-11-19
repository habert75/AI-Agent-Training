import os
from huggingface_hub import InferenceClient
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ.get("HF_TOKEN"),
)

response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3", 
	messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
	max_tokens=500,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)