# Anthropic Claude ReAct AI Agent

A proper **ReAct (Reason and Act)** agent implementation using Anthropic Claude that handles multiple tool calls in a loop.

## Key Features

- **Multiple Tool Calls**: Processes ALL tool calls in each response
- **Iterative Reasoning**: Continues until Claude returns a final answer
- **Anthropic API**: Uses Claude's native tool calling format
- **Complete Context**: Maintains full conversation history

## API Differences from OpenAI

- **Tool Schema**: Uses `input_schema` instead of `parameters`
- **Response Format**: Tools are in `content` array with `type: "tool_use"`
- **Tool Results**: Uses `tool_use_id` instead of `tool_call_id`
- **Message Structure**: Tool results go in user messages with `content` array

## Examples

Same examples as OpenAI version but using Claude's API format.

# Run

## Run directly

`uv run main.py` (or alternative files)

## Run indirectly

Create a virtual environment

```bash
uv venv
```

Activate virtual environment

```bash
source .venv/bin/activate
```

Install packages

```bash
uv sync
```

Run script main (or alternative files)

```bash
python main.py
```
