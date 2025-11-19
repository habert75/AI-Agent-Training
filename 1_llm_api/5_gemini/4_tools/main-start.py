import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

tools = [
    {
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
    {
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
]

# Configure the client and tools
client = genai.Client(api_key=api_key)
gemini_tools = types.Tool(function_declarations=tools)
config = types.GenerateContentConfig(tools=[gemini_tools])

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the current stock price for MSFT?",
    config=config,
)

print("--- Full response: ---")
print(response)
print("--- Response text: ---")
print(response.text)
print("--- Response Tool call: ---")
print(response.candidates[0].content.parts[0].function_call)
