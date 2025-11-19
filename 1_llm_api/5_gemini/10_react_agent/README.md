# Google Gemini ReAct AI Agent

A proper **ReAct (Reason and Act)** agent implementation using Google Gemini that handles multiple function calls in a loop.

## Key Features

- **Google Gemini**: Uses Gemini 2.5 Flash model
- **Multiple Function Calls**: Processes ALL function calls in each response
- **Unique API**: Different conversation format from other providers
- **Function Responses**: Uses specialized FunctionResponse objects

## API Differences from OpenAI

- **Content Format**: Uses `contents` array instead of `messages`
- **Function Calls**: Located in `part.function_call` within content parts
- **Function Responses**: Uses `types.FunctionResponse` objects
- **Configuration**: Tools configured via `GenerateContentConfig`

## Examples

Same examples as other versions but adapted for Gemini's unique API format.

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
