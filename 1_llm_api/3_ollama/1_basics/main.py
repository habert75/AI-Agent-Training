from ollama import chat
from ollama import ChatResponse
from pprint import pprint

for _ in range(10):
    response: ChatResponse = chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant.",
            },
            {
                "role": "user",
                "content": "Give me random number.",
            },
        ],
    )

    # print("--- Full response: ---")
    # pprint(response)
    print("--- Response text: ---")
    print(response.message.content)
