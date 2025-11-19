import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Use this function to get the current price of a stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker symbol for the stock, e.g. GOOG",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_dividend_date",
            "description": "Use this function to get the next dividend payment date of a stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker symbol for the stock, e.g. GOOG",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
]


data = {
    "model": "gpt-4o",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "What is the current stock price for MSFT?"},
    ],
    "tools": tools,  # CUSTOM TOOLS
    "tool_choice": "auto",
}


response = requests.post(
    "https://api.openai.com/v1/chat/completions", headers=headers, json=data
)

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["message"]["content"])
