# HuggingFace ReAct AI Agent

A proper **ReAct (Reason and Act)** agent implementation using HuggingFace models via their OpenAI-compatible API.

## Key Features

- **HuggingFace Models**: Access to open-source models like Llama
- **OpenAI-Compatible**: Uses familiar OpenAI API format
- **Multiple Tool Calls**: Processes ALL tool calls in each response
- **Cost-Effective**: Often cheaper than proprietary APIs

## API Details

- **Endpoint**: `https://router.huggingface.co/hf-inference/v1`
- **Format**: Same as OpenAI (tool_calls, tool_call_id, etc.)
- **Models**: Llama, Mistral, and other open-source models
- **Authentication**: Uses HF_TOKEN instead of OpenAI API key

## Examples

Same examples as OpenAI version but using HuggingFace's model router.

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
