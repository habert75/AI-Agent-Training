import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simple  "tool" - adds up numbers
def compute_sum(numbers: list):
    return {"numbers": numbers, "sum": sum(numbers)}

tools = [
    {
        "type": "function",
        "function": {
            "name": "compute_sum",
            "description": "add up the list of numbers and return the sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "The list of numbers to sum up.",
                    }
                },
                "required": ["numbers"],
            },
        }
    }
]

available_functions = {"compute_sum": compute_sum}

def run_dialog(messages, model="gpt-4o"):
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    msg = resp.choices[0].message
    print("First model message:", msg)

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        fname = tool_call.function.name
        fargs = json.loads(tool_call.function.arguments)
        tool_id = tool_call.id

        result = available_functions[fname](**fargs)
        print("Tool result:", result)

        # adding message representing calling tool and its result
        messages.append({
            "role": "assistant",
            "tool_calls": [
                {"id": tool_id, "type": "function", "function": {"name": fname, "arguments": json.dumps(fargs)}}
            ]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_id,
            "name": fname,
            "content": json.dumps(result),
        })

        # repetition of the modal call for final reponse 
        final = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        return final.choices[0].message

    return msg

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "please sum up the following numbers: 4, 7, 10, 1."},
    ]
    final_msg = run_dialog(messages)
    print("--- Final message ---")
    print(final_msg)
    # text of the response if it exists
    print("--- Final message content ---")
    print(final_msg.content if hasattr(final_msg, "content") else "")