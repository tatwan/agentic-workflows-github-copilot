# examples/

Customization files to copy into your own repository. Each one is short on purpose: read it, change it for
your team, and test it before you share it.

| File | What it is | Where it goes | Read by |
|---|---|---|---|
| `instructions/python.instructions.md` | Instructions for Python files only (`applyTo`) | `.github/instructions/` | VS Code, Copilot CLI, cloud agent |
| `skills/release-notes/` | A skill that drafts release notes from merged pull requests | `.github/skills/` | VS Code, Copilot CLI, cloud agent |
| `agents/test-explainer.agent.md` | A read-only custom agent that explains a failing test | `.github/agents/` | VS Code, Copilot CLI, cloud agent |

What each kind of file is for, and when to choose it: [guides/customization-options.md](../guides/customization-options.md).

Lab 05, Part E installs `skills/release-notes` the way a team shares a skill: by copying the folder.

The files you write in the labs are not here: Lab 04 writes two instructions files, Lab 05 the `meeting-actions`
skill and Lab 06 a reviewer agent, each inside that lab's `project/.github/` folder.
