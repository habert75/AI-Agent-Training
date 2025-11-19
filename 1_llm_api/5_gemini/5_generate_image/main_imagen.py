from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# Only for PAID users
# ------------------------------------------------------------------
# ------------------------------------------------------------------

client = genai.Client()

contents = "Generate and image of Black Subaru Impreza WRX STI in a countryside in Czech Republic?"

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=contents,
    config=types.GenerateImagesConfig(
        number_of_images=4,
    ),
)

i = 0
for generated_image in response.generated_images:
    i += 1
    image = Image.open(BytesIO(generated_image.image.image_bytes))
    image.save(f"generated_image_{i}.png")
    image.show()
