import json
import yfinance as yf
from ollama import chat, ChatResponse
from typing import List, Dict, Any

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

# Define tools for Ollama (mixed format as shown in original)
tools = [
    get_stock_price,  # Direct function reference
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

# Available functions for calling
available_functions = {
    "get_stock_price": get_stock_price,
    "get_dividend_date": get_dividend_date,
}


class OllamaReactAgent:
    """A ReAct (Reason and Act) agent using Ollama."""
    
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.max_iterations = 10
        
    def run(self, messages: List[Dict[str, Any]]) -> str:
        """
        Run the ReAct loop until we get a final answer.
        """
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Call the LLM
            response: ChatResponse = chat(
                self.model,
                messages=messages,
                tools=tools,
            )
            
            print(f"LLM Response: {response.message}")
            
            # Check if there are tool calls
            if response.message.tool_calls:
                # Add the assistant's message to history
                messages.append(response.message)
                
                # Process ALL tool calls
                for tool_call in response.message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = tool_call.function.arguments
                    
                    print(f"Executing tool: {function_name}({function_args})")
                    
                    # Call the function
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(**function_args)
                    
                    print(f"Tool result: {function_response}")
                    
                    # Add tool response to messages
                    messages.append({
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    })
                
                # Continue the loop to get the next response
                continue
                
            else:
                # No tool calls - we have our final answer
                final_content = response.message.content
                
                # Add the final assistant message to history
                messages.append(response.message)
                
                print(f"\nFinal answer: {final_content}")
                return final_content
        
        # If we hit max iterations, return an error
        return "Error: Maximum iterations reached without getting a final answer."


def main():
    # Create a ReAct agent
    agent = OllamaReactAgent()
    
    # Example 1: Simple query (single tool call)
    print("=== Example 1: Single Tool Call ===")
    messages1 = [
        {"role": "user", "content": "What is the current stock price for MSFT?"}
    ]
    
    result1 = agent.run(messages1.copy())
    print(f"\nResult: {result1}")
    
    # Example 2: Complex query requiring multiple tool calls
    print("\n\n=== Example 2: Multiple Tool Calls ===")
    messages2 = [
        {"role": "user", "content": "What are the current prices and dividend dates for both MSFT and AAPL? Please provide a summary."}
    ]
    
    result2 = agent.run(messages2.copy())
    print(f"\nResult: {result2}")
    
    # Example 3: Sequential reasoning
    print("\n\n=== Example 3: Sequential Reasoning ===")
    messages3 = [
        {"role": "user", "content": "Compare the stock prices of GOOGL and META. Which one is more expensive?"}
    ]
    
    result3 = agent.run(messages3.copy())
    print(f"\nResult: {result3}")


if __name__ == "__main__":
    main()