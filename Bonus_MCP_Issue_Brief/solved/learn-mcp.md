# Microsoft Learn MCP brief

Prepared example checked 14 October 2026 against the
[Microsoft Learn MCP overview](https://learn.microsoft.com/en-us/training/support/mcp).

| Fact | Source |
|---|---|
| Endpoint is `https://learn.microsoft.com/api/mcp` | Overview, How the server works |
| It uses Streamable HTTP | Overview, How the server works |
| Access requires no authentication | Overview, Requirements |

A direct MCP tools-list check exposed `microsoft_docs_search`, `microsoft_code_sample_search` and
`microsoft_docs_fetch`. Tool availability can change. Check your own client rather than treating this list as a
fixed contract. A proposed next check is to search for a topic, fetch a returned page, and compare the answer with
that page. This proposed check is separate from the source facts.
