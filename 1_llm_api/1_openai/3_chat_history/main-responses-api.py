import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() 

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response = client.responses.create(
    model="gpt-4o",
    instructions="You are an AI assistant",
    input="Tell me a joke.",
)

print("--- Full response: ---")
print(response)
print("--- Response text: ---")
print(response.output_text)


response2 = client.responses.create(
    model="gpt-4o",
    instructions="You are an AI assistant",
    input="What was the joke you just told me?",
    previous_response_id=response.id
)

print("--- Full response: ---")
print(response2)
print("--- Response text: ---")
print(response2.output_text)