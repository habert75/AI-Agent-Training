import os
import asyncio
from dotenv import load_dotenv
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

import chromadb

load_dotenv()


def get_tavily_mcp_url() -> str:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment")
    return f"https://mcp.tavily.com/mcp/?tavilyApiKey={api_key}"


async def get_mcp_tools():
    """Load tools from Tavily MCP server and return (tools, client)."""
    client = MultiServerMCPClient(
        {
            "tavily": {
                "url": get_tavily_mcp_url(),
                "transport": "streamable_http",
            }
        }
    )
    tools = await client.get_tools()
    return tools, client


# Global handle set at runtime in main
_MCP_CLIENT = None
_MCP_TOOLS = []


def query_chroma(name: str, query: str) -> List[str]:
    chroma_path = os.getenv("CHROMA_PATH", "./chroma_db")
    try:
        client = chromadb.PersistentClient(path=chroma_path)
    except Exception:
        client = chromadb.Client()

    docs: List[str] = []
    try:
        # attempt to list collections
        try:
            collections = [c.name for c in client.list_collections()]
        except Exception:
            try:
                collections = [c["name"] for c in client.list_collections()]
            except Exception:
                collections = []

        if not collections:
            collections = ["Students", "people", "profiles", "policies"]

        for coll in collections:
            try:
                col = client.get_or_create_collection(name=coll)
                res = col.query(query_texts=[f"{name} {query}"], n_results=3)
                documents = res.get("documents") if isinstance(res, dict) else None
                if documents:
                    for d in documents:
                        if isinstance(d, list):
                            docs.extend(d)
                        else:
                            docs.append(str(d))
            except Exception:
                continue
    except Exception:
        pass

    return docs


@tool
def get_individual_info(name: str, query: str) -> str:
    """Tool that retrieves info from Chroma DB and the Tavily MCP tools, then saves a TXT file.

    This tool is intentionally best-effort: it will try to call available MCP tools
    and record any responses. The resulting combined text is saved to
    `<name>_combined.txt` in the current working directory and the file path
    is returned.
    """
    # Chroma retrieval
    chroma_docs = query_chroma(name, query)

    # MCP tool calls (best-effort)
    mcp_results: List[Dict[str, Any]] = []
    try:
        tools = _MCP_TOOLS or []
        for t in tools:
            tname = getattr(t, "name", None) or getattr(t, "__name__", None) or str(t)
            target = getattr(t, "func", t)
            try:
                if callable(target):
                    # try calling with the combined input string
                    inp = f"{name} {query}"
                    if asyncio.iscoroutinefunction(target):
                        res = asyncio.run(target(inp))
                    else:
                        # Some tool functions accept different signatures; try simple call
                        try:
                            res = target(inp)
                        except TypeError:
                            # try calling without args
                            res = target()
                else:
                    res = {"error": "not callable"}
            except Exception as e:
                res = {"error": str(e)}

            mcp_results.append({"tool": str(tname), "result": res})
    except Exception as e:
        mcp_results.append({"tool": "mcp_client_error", "result": str(e)})

    # Combine and save
    parts = [f"Name: {name}\nQuery: {query}\n", "--- Chroma ---\n"]
    if chroma_docs:
        parts.extend([str(d) + "\n" for d in chroma_docs])
    else:
        parts.append("No chroma docs found.\n")

    parts.append("--- MCP ---\n")
    if mcp_results:
        for r in mcp_results:
            parts.append(f"Tool: {r.get('tool')}\nResult:\n{r.get('result')}\n\n")
    else:
        parts.append("No MCP results.\n")

    combined = "\n".join(parts)
    safe = (name or "unknown").replace(" ", "_")
    out = os.path.join(os.getcwd(), f"{safe}_combined.txt")
    try:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(combined)
    except Exception as e:
        return f"Failed to save combined file: {e}"

    return f"Saved combined data to: {out}"


async def main():
    global _MCP_CLIENT, _MCP_TOOLS

    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5-mini"))

    print("Initializing MCP connection to Tavily...")
    mcp_tools, mcp_client = await get_mcp_tools()
    _MCP_CLIENT = mcp_client
    _MCP_TOOLS = list(mcp_tools)
    print(f"Loaded {len(_MCP_TOOLS)} tools from Tavily MCP\\n")

    # Combine tools: prefer MCP tools first so agent can call them, then our high-level tool
    tools = list(_MCP_TOOLS) + [get_individual_info]

    # Print tool summary
    import inspect

    for t in tools:
        name = getattr(t, "name", None) or getattr(t, "__name__", None) or type(t).__name__
        desc = getattr(t, "description", "") or getattr(t, "desc", "")
        target = getattr(t, "func", t)
        sig = ""
        if callable(target):
            try:
                sig = str(inspect.signature(target))
            except Exception:
                sig = ""
        print(f"{name}{sig} - {desc}")

    # Create agent
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="You are a helpful assistant. Use available tools to fetch factual data about an individual and save combined results when requested.",
    )

    # Interactive loop
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        result = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
        print("Assistant:", result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
