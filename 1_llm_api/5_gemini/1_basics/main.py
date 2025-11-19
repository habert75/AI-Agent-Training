from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Tell me a joke.",
)

print("--- Full response: ---")
print(response)
print("--- Response text: ---")
print(response.text)
