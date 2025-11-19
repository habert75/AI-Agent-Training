from ollama import Client
from pprint import pprint

client = Client(host="http://localhost:11434")

response = client.embed(
    model="all-minilm:l6-v2",
    input="Llamas are members of the camelid family",
)

print("--- Full response: ---")
pprint(response)
