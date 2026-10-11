# examples/

Customization files to copy into your own repository. Each one is short on purpose: read it, change it for
your team, and test it before you share it.

| File | What it is | Where it goes | Read by |
|---|---|---|---|
| `instructions/python.instructions.md` | Instructions for Python files only (`applyTo`) | `.github/instructions/` | VS Code, Copilot CLI, cloud agent |
| `skills/release-notes/` | A skill that drafts release notes from merged pull requests; Lab 05 installs it | `.github/skills/` | VS Code, Copilot CLI, cloud agent |
| `agents/test-explainer.agent.md` | A read-only custom agent that explains a failing test | `.github/agents/` | VS Code, Copilot CLI, cloud agent |
| `prompts/pr-summary.prompt.md` | A prompt file. **Legacy:** loads only in the Local harness and is deprecated for the Copilot harness; prefer a skill | `.github/prompts/` | VS Code Local harness only |

What each kind of file is for, and when to choose it: [guides/customization-options.md](../guides/customization-options.md).

The files you write in the labs (`sql-review`, `reviewer.agent.md`, `perf-report.agent.md`, the PreToolUse
hook) are not here. Their reference versions will live in each lab’s gitignored `solved/` folder as the labs are built.
