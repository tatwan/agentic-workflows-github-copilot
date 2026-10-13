# Customization options: which file to change

Checked 6 Oct 2026 against VS Code 1.140 and GitHub Docs. Copilot changes monthly; check the VS Code docs
before you rely on a detail here.

## Start from the problem you keep seeing

VS Code's own advice is to make the smallest change that fixes a repeated problem.

| What keeps happening | Smallest change | File |
|---|---|---|
| It misses a one-time requirement | Say it in the request | none |
| It keeps missing a project convention | Instructions | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `AGENTS.md` |
| The team keeps explaining the same multi-step process | A skill | `.github/skills/<name>/SKILL.md` |
| A recurring role needs a restricted tool set | A custom agent | `.github/agents/<name>.agent.md` |
| It needs an external system | An MCP server | `.mcp.json` at the repository root |
| An action must run whatever the model decides | A hook | `.github/hooks/*.json` |

## What each one does

**Instructions** are added to every request in the repository (`copilot-instructions.md`, `AGENTS.md`), or
when a changed file matches `applyTo` or the file's description matches the task (`*.instructions.md`). They guide the model; they do not enforce
anything. Every request re-sends them, so a long file costs credits on every turn. `/init` in a Local session
drafts one from the repository. [Lab 04](../04_Team_Rules/) writes a `copilot-instructions.md` and a `reviews.instructions.md`.

**A skill** is a folder with a `SKILL.md` (a `name`, a `description` and instructions), plus optional scripts
and reference files. Copilot reads only the name and description until a task matches, then loads the rest.
The name must match the folder: lowercase letters, numbers and hyphens, 64 characters at most; the
description 1,024 characters at most. Skills also run as slash commands ([Lab 05](../05_Make_A_Skill/) runs `/meeting-actions`). Project folders:
`.github/skills/`, `.claude/skills/`, `.agents/skills/`; personal folders: `~/.copilot/skills/`,
`~/.claude/skills/`, `~/.agents/skills/`. Example: `examples/skills/release-notes/`.

**A custom agent** is an `.agent.md` file that gives Copilot a role: instructions, a model and the tools it may
use. A `tools:` list of `['read', 'search']` makes a reviewer that cannot change a file however it is asked.
`handoffs` add a button that passes the work to another agent with a prompt filled in. Example:
`examples/agents/test-explainer.agent.md`.

**A hook** is a command VS Code runs at a fixed point in a session, such as before every tool call. A
PreToolUse hook can allow, deny or ask. Hooks are Preview in VS Code; try one in a test workspace first.

**Prompt files** (`.prompt.md`) still load in the Local harness but are deprecated for the Copilot harness.
Write a skill instead.

## Where each one is read

| | VS Code, Local | VS Code, Copilot harness | Copilot CLI | Copilot cloud agent |
|---|---|---|---|---|
| Instructions, skills, custom agents | yes | yes | yes | yes |
| Prompt files | yes, for now | no | no | no |
| Handoffs | yes | yes | not documented | ignored |

## How to tell whether it worked

- `/skills` lists the skills configured for the workspace.
- Agent Debug Logs (Preview) show which instructions files loaded and, under Discovery, whether a skill was
  found, skipped or rejected, with the reason.
- The Chat Debug view for one request shows what was sent: if the skill's instructions are in it, the skill
  was used.

Keep these files in the repository and review them like code, with one owner each. Before and after a change,
compare a few measures on real tasks: review rework, time from pull request to merge, how often a skill loads
when it should, credits per merged pull request.
