# Retail Assistant Agent (with Slack)

This n8n workflow runs an AI agent that queries an Elasticsearch dataset and posts concise summaries to Slack.


Configuration
- Slack credential: create a Slack credential in n8n 
- Elasticsearch credential: ensure Elasticsearch account is configured in n8n credentials.
- OpenAI credential: ensure the OpenAi account credential is present and has sufficient rate limits.

Key behavior and safety
- The agent is instructed (system message) to return tool-call JSON only when invoking tools (no extra commentary).
- The `Format Slack message` node extracts agent output safely, prefers `output`, `input.text`, `text`, `body`, `message`, or top results from `results`/`hits` arrays, then truncates to 2000 characters.
- The default Slack channel is `#all-ai-agents`. Change this in the Slack node or make the agent return a different channel in the tool call.
- To avoid OpenAI rate-limit/token errors, the system prompt asks the agent to summarize results (max ~400 tokens) and not to return full document dumps.

Steps how to run the flow:
1. Import or open `Retail Assistant Agent.json` in n8n.
2. Configure credentials (Slack, Elasticsearch, OpenAI) in n8n.
3. Run a test chat message via the agent trigger or use the n8n Test UI.
4. Inspect the `Format Slack message` node execution data to verify `{ channel, text }