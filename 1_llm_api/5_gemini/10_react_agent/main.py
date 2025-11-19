import os
import json
import yfinance as yf
from google import genai
from google.genai import types
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Initialize Gemini client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Function Implementations
def get_stock_price(ticker: str):
    """Get the current price of a stock."""
    ticker_info = yf.Ticker(ticker).info
    current_price = ticker_info.get("currentPrice")
    return {"ticker": ticker, "current_price": current_price}


def get_dividend_date(ticker: str):
    """Get the next dividend payment date of a stock."""
    ticker_info = yf.Ticker(ticker).info
    dividend_date = ticker_info.get("dividendDate")
    return {"ticker": ticker, "dividend_date": dividend_date}

# Define tools for Gemini
tools_schema = [
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

available_functions = {
    "get_stock_price": get_stock_price,
    "get_dividend_date": get_dividend_date,
}

# Configure tools for Gemini
gemini_tools = types.Tool(function_declarations=tools_schema)


class GeminiReactAgent:
    """A ReAct (Reason and Act) agent using Google Gemini."""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.max_iterations = 10
        
    def run(self, initial_query: str) -> str:
        """
        Run the ReAct loop until we get a final answer.
        Note: Gemini API uses a different conversation format
        """
        iteration = 0
        contents = [initial_query]  # Start with user query
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Create config with tools
            config = types.GenerateContentConfig(tools=[gemini_tools])
            
            # Call the LLM
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )
            
            print(f"LLM Response: {response}")
            
            # Check if there are function calls
            has_function_calls = False
            function_calls = []
            
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    has_function_calls = True
                    function_calls.append(part.function_call)
            
            if has_function_calls:
                # Add model response to contents
                contents.append(response.candidates[0].content)
                
                # Process ALL function calls
                function_responses = []
                for function_call in function_calls:
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    print(f"Executing tool: {function_name}({function_args})")
                    
                    # Call the function
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(**function_args)
                    
                    print(f"Tool result: {function_response}")
                    
                    # Create function response for Gemini format
                    func_response = types.FunctionResponse(
                        name=function_name,
                        response=function_response
                    )
                    function_responses.append(func_response)
                
                # Add all function responses as a single content part
                contents.append(types.Content(
                    parts=[types.Part(function_response=fr) for fr in function_responses]
                ))
                
                # Continue the loop to get the next response
                continue
                
            else:
                # No function calls - we have our final answer
                final_content = response.text
                
                print(f"\nFinal answer: {final_content}")
                return final_content
        
        # If we hit max iterations, return an error
        return "Error: Maximum iterations reached without getting a final answer."


def main():
    # Create a ReAct agent
    agent = GeminiReactAgent()
    
    # Example 1: Simple query (single tool call)
    print("=== Example 1: Single Tool Call ===")
    result1 = agent.run("What is the current stock price for MSFT?")
    print(f"\nResult: {result1}")
    
    # Example 2: Complex query requiring multiple tool calls
    print("\n\n=== Example 2: Multiple Tool Calls ===")
    result2 = agent.run("What are the current prices and dividend dates for both MSFT and AAPL? Please provide a summary.")
    print(f"\nResult: {result2}")
    
    # Example 3: Sequential reasoning
    print("\n\n=== Example 3: Sequential Reasoning ===")
    result3 = agent.run("Compare the stock prices of GOOGL and META. Which one is more expensive?")
    print(f"\nResult: {result3}")


if __name__ == "__main__":
    main()