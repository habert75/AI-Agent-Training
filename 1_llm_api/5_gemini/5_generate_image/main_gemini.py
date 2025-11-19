from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key, http_options=types.HttpOptions(api_version="v1"))

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# Does not work with the latest google.genai SDK
# ------------------------------------------------------------------
# ------------------------------------------------------------------


print("Available Models (using newer google.genai SDK):")
# In the newer SDK, you typically access models via client.models
# and then call methods like list() or get() on that. [4, 5, 6]
for m in client.models.list():  # [4, 5, 6]
    # The 'models' endpoint provides metadata like supported functionality. [6]
    # If you want to check for generateContent, you'd look at m.supported_methods
    if "generateContent" in m.supported_actions:
        print(f"- {m.name} (Supports generateContent)")
    # You can also print all supported methods for a model
    # print(f"- {m.name}, Supported Methods: {m.supported_methods}")


contents = (
    "Hi, can you create a 3d rendered image of a pig "
    "with wings and a top hat flying over a happy "
    "futuristic scifi city with lots of greenery?"
)

response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO((part.inline_data.data)))
        image.save("gemini-native-image.png")
        image.show()
