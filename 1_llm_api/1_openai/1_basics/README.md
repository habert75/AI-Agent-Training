# Description

Ways to communicate with OpenAI ordered from oldest to newest:

1. Http
2. Text completion API (Deprecated) - https://platform.openai.com/docs/api-reference/completions
3. Chat completion API - https://platform.openai.com/docs/api-reference/chat
4. Responses API - https://platform.openai.com/docs/api-reference/responses/create

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
