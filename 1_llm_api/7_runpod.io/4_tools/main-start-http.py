import os
import requests
from pprint import pprint

headers = {"Content-Type": "application/json"}

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


# lukaskellerstein/tools-mistral-16bit-merged-new
# mistralai/Mistral-7B-Instruct-v0.3
data = {
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "What is the current stock price for MSFT?"},
    ],
    "tools": tools,  # CUSTOM TOOLS
    "tool_choice": "auto",
}

for i in range(10):

    response = requests.post(
        "https://ttt0nkhw3r2tz3-8080.proxy.runpod.net/v1/chat/completions",
        headers=headers,
        json=data,
    )

    # print("--- Full response: ---")
    # pprint(response.json())
    print("--- Response text: ---")
    print(response.json()["choices"][0]["message"])
