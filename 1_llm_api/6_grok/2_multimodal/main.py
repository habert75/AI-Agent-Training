import os
from pprint import pprint
from encode import encode_image
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() 

client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key=os.environ.get("GROK_API_KEY"),
)

response = client.chat.completions.create(
    model="grok-2-vision-1212",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {
            "role": "user",
            "content":  [
                {
                    "type": "text",
                    "text": "What is in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image("./test_image.png")}",
                    }
                }
            ]
        },
    ],
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)