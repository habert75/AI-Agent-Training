# Background Check Agent

This directory contains `background_check_agent.py`, an agent that:
- Retrieves documents about an individual from a ChromaDB vector store.
- Queries Tavily MCP tools (best-effort) for additional information.
- Combines results and saves them to `<Name>_combined.txt` in the current working directory.

Prerequisites
- Python 3.10+ recommended
- A Python environment with these packages installed (example):
  pip install chromadb python-dotenv langchain-openai langchain_mcp_adapters langchain_core langchain

Environment
- Create a `.env` file (or set env vars) with at least:
  - `TAVILY_API_KEY` — required to connect to the Tavily MCP server.
  - Optional: `CHROMA_PATH` — path to persistent Chroma DB (defaults to `./chroma_db`).
  - Optional: `OPENAI_MODEL` — model name used by the agent (defaults to `gpt-5-mini`).

