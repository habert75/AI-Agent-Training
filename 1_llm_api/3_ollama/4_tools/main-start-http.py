from pprint import pprint
import json
import requests

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
    "model": "mistral",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {
            "role": "user",
            "content": "What is the current stock price for MSFT?",
        },
    ],
    "tools": tools,  # CUSTOM TOOLS
    "tool_choice": "auto",
    "stream": False,
}

response = requests.post("http://localhost:11434/api/chat", data=json.dumps(data))

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["message"])
