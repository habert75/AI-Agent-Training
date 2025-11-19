import os
import json
import yfinance as yf
import anthropic
from pprint import pprint
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

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

# Define custom tools
tools = [
    {
        "name": "get_stock_price",
        "description": "Use this function to get the current price of a stock.",
        "input_schema": {
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
        "input_schema": {
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


class AnthropicReactAgent:
    """A ReAct (Reason and Act) agent using Anthropic Claude."""
    
    def __init__(self, model: str = "claude-3-7-sonnet-20250219"):
        self.model = model
        self.max_iterations = 10
        
    def run(self, messages: List[Dict[str, Any]], system_prompt: str = "You are a helpful AI assistant.") -> str:
        """
        Run the ReAct loop until we get a final answer.
        """
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Call the LLM
            response = client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                tools=tools,
                tool_choice={"type": "auto"}
            )
            
            print(f"LLM Response: {response}")
            
            # Check if there are tool calls in the response
            has_tool_calls = any(item.type == "tool_use" for item in response.content)
            
            if has_tool_calls:
                # Extract all tool calls
                tool_calls = [item for item in response.content if item.type == "tool_use"]
                
                # Add the assistant's message with tool calls to history
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # Process ALL tool calls
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.name
                    function_args = tool_call.input
                    tool_id = tool_call.id
                    
                    print(f"Executing tool: {function_name}({function_args})")
                    
                    # Call the function
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(**function_args)
                    
                    print(f"Tool result: {function_response}")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": json.dumps(function_response)
                    })
                
                # Add all tool results to messages
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
                
                # Continue the loop to get the next response
                continue
                
            else:
                # No tool calls - we have our final answer
                final_content = ""
                for item in response.content:
                    if hasattr(item, 'text'):
                        final_content += item.text
                
                # Add the final assistant message to history
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                print(f"\nFinal answer: {final_content}")
                return final_content
        
        # If we hit max iterations, return an error
        return "Error: Maximum iterations reached without getting a final answer."


def main():
    # Create a ReAct agent
    agent = AnthropicReactAgent()
    
    # Example 1: Simple query (single tool call)
    print("=== Example 1: Single Tool Call ===")
    messages1 = [
        {"role": "user", "content": "What is the current stock price for MSFT?"},
    ]
    
    result1 = agent.run(messages1.copy())
    print(f"\nResult: {result1}")
    
    # Example 2: Complex query requiring multiple tool calls
    print("\n\n=== Example 2: Multiple Tool Calls ===")
    messages2 = [
        {"role": "user", "content": "What are the current prices and dividend dates for both MSFT and AAPL? Please provide a summary."},
    ]
    
    result2 = agent.run(messages2.copy())
    print(f"\nResult: {result2}")
    
    # Example 3: Sequential reasoning
    print("\n\n=== Example 3: Sequential Reasoning ===")
    messages3 = [
        {"role": "user", "content": "Compare the stock prices of GOOGL and META. Which one is more expensive?"},
    ]
    
    result3 = agent.run(messages3.copy())
    print(f"\nResult: {result3}")


if __name__ == "__main__":
    main()