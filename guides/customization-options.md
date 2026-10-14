# Customization options: which file to change

Checked 14 October 2026 against the linked official documentation. Names and support differ by Copilot client,
session type and organisation policy. The labs use VS Code; check another client's documentation before moving
optional fields or controls there.

## Start with the recurring problem

| What you need | Use | Workspace location in these labs | Try it |
|---|---|---|---|
| A requirement for one task | A request, with the relevant context | Chat input | [02](../02_Plan_Then_Build/) |
| A convention for the whole project | Project instructions | `.github/copilot-instructions.md` | [04](../04_Team_Rules/) |
| Rules for matching files | Scoped instructions with `applyTo` | `.github/instructions/*.instructions.md` | [04](../04_Team_Rules/) |
| A repeatable procedure with resources | A skill | `.github/skills/<name>/SKILL.md` | [05](../05_Make_A_Skill/) |
| A selected role with a particular tool set | A custom agent | `.github/agents/<name>.agent.md` | [06](../06_Agent_With_Limits/) |
| Access to another system's tools or data | An MCP server | `.mcp.json`, with `mcpServers` | [MCP bonus](../Bonus_MCP_Issue_Brief/) |

Instructions supply the baseline. Skills supply task methods. Custom agents select roles and tools. MCP connects
to external capabilities. You can combine them, but start with the smallest change that solves the repeated
problem. A skill that explains a workflow does not create an external connection by itself.

## Review what you install

A skill has `name` and `description` in its frontmatter, then the steps. The description helps Copilot decide when
to load it; selecting its `/name` command requests it explicitly. Keep linked templates and scripts in the same
folder and review them too. [Lab 05](../05_Make_A_Skill/) uses a template and a new notes file to check reuse.
Optional fields such as `allowed-tools` are not a portable security boundary.

A custom agent adds a role and a tool list. In [Lab 06](../06_Agent_With_Limits/), `read` and `search` leave the
reviewer without editing or execution tools. Check the tools actually exposed in your session. Adding `execute`
permits commands that can write files even if `edit` is absent. Handoffs, where supported, can pass a prepared
request to another agent; inspect the destination and permissions before using one.

The MCP bonus requests an issue-reading tool and GitHub's server-side read-only filter. That filter belongs to
that server; it does not restrict another connector or a terminal. The older VS Code configuration at
`.vscode/mcp.json` uses a `servers` object. The portable `.mcp.json` uses `mcpServers`. Keep secrets out of both.

## Check whether the change worked

1. Find the file or server in **Configure Chat**. This establishes discovery.
2. Inspect the request's steps, References where available, or debug details for loading/invocation and tool use.
3. Check the actual output and files against the task. A loaded rule can still be ignored.
4. Repeat in a New Chat with a new input. Move earlier answers outside the workspace so the agent cannot copy
   them. Try an unrelated task too: the specialized procedure should stay out of it.

Project instructions are guidance. Tool restrictions, server controls and approval settings decide access at
other layers. Keep each claim tied to the control that actually provides it.

## Resources

- [Instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [MCP servers](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
