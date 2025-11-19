from PIL import Image
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

image = Image.open("./test_image.png")
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=[image, "What is in this image?"]
)
print("--- Full response: ---")
print(response)
print("--- Response text: ---")
print(response.text)
