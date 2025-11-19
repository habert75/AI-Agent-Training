# xAI Grok ReAct AI Agent

A proper **ReAct (Reason and Act)** agent implementation using xAI Grok that handles multiple tool calls in a loop.

## Key Features

- **xAI Grok**: Uses Grok-3-mini model
- **OpenAI-Compatible**: Same API format as OpenAI
- **Multiple Tool Calls**: Processes ALL tool calls in each response
- **Real-time Data**: Grok has access to real-time information

## API Details

- **Endpoint**: `https://api.x.ai/v1`
- **Format**: Identical to OpenAI (tool_calls, tool_call_id, etc.)
- **Models**: grok-3-mini, grok-3-pro
- **Authentication**: Uses GROK_API_KEY

## Examples

Same examples as OpenAI version but using Grok's models with potential real-time data access.

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
