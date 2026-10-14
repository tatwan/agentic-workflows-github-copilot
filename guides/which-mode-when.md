# Which way of working: pick by the task

Checked 14 Oct 2026 against the VS Code docs. Copilot changes monthly, and your organisation may have turned some of
these off; check the VS Code docs before you rely on a detail here.

Copilot in VS Code offers several ways to work, from a suggestion as you type to an agent that opens a pull request
while you do something else. They differ in two things: **how much Copilot decides on its own**, and **when you
check its work**. Pick the smallest one that does the job; broader work can add usage and leave more for you to review.

## Start from the task

| You want to | Use | You check | Lab |
|---|---|---|---|
| Finish the line or block you are typing | **Inline suggestions** (grey text; Tab accepts) and **next edit suggestions** (the related edit it offers next) | Each suggestion, before you accept it | — |
| Change or explain the code you have selected, right where it is | **Inline chat**: Ctrl+I (Cmd+I on macOS) in the editor | The diff in the editor: Keep or Undo | [00](../00_Setup_Check/), last section |
| Write a commit message, rename a symbol, fix one error | The sparkle actions in Source Control and in the editor's right-click menu | The message or the change | — |
| Understand a project, research a question, or decide how before anything changes | **Ask** for an explanation where available; **Plan** for an implementation approach: inspect its actions and plan artifact | The answer or the plan, before you act on it | [01](../01_How_An_Agent_Works/), [02](../02_Plan_Then_Build/) |
| A change across files, with a check that shows whether it worked | **Interactive** (or **Agent**) with **Manual permissions**: edits files, stops before most commands | The plan, each command before it runs, the diff and the result | [01](../01_How_An_Agent_Works/)–[03](../03_Fix_A_Data_Pipeline/), [07](../07_Organize_Files_And_Notes/), [08](../08_Analyze_Data_And_Cost/) |
| A longer change with a check you already trust | **Autopilot**: carries on with fewer stops | The diff and the result at the end | [01](../01_How_An_Agent_Works/) and [02](../02_Plan_Then_Build/), Going further |
| A job the team repeats, done the same way each time | A **skill**, called with `/name` | The output against the method | [05](../05_Make_A_Skill/) |
| A role that must never edit or run anything | A **custom agent** with a short tool list | The files, not its reply | [06](../06_Agent_With_Limits/) |
| A well-scoped issue you will review later as a pull request | The **cloud agent**: the Cloud session target in VS Code, or assign the issue to Copilot on GitHub | The pull request, like anyone's | [02](../02_Plan_Then_Build/), Going further |
| A second opinion on a pull request | **Copilot code review** on GitHub | Its comments, as you would a colleague's | [02](../02_Plan_Then_Build/), Going further |

Inline suggestions and next edit suggestions are not billed in AI credits; chat and agent requests are
([saving tokens](saving-tokens.md)).

## Three questions that settle most choices

1. **Do you want an answer or a change?** An answer: Ask where available, or a brief read-only request. An implementation approach: Plan. A change: Interactive (or Agent), or inline
   chat if the change is in front of you.
2. **Can you tell, quickly, whether the result is right?** If yes, let the agent act and run the check. If not,
   work out the check first, as every lab's Part A does, or ask for a plan before any change.
3. **Could a mistake be hard to undo?** Restore Checkpoint undoes the agent's edits, not the commands it ran
   ([Lab 07](../07_Organize_Files_And_Notes/)). Keep Manual permissions, approve commands once, and work in small
   batches.

## Give it the context it needs, and only that

The agent finds files by searching, but you can hand it what it needs and save a few reads:

- Type `#` in the chat input to attach a file, a folder, a symbol, terminal output or your source control changes.
- Select **Add Context** in the Chat view, or drag files from the Explorer onto the chat.
- Select code in the editor before you ask, and the selection goes with the request.
- Attach a screenshot, or paste a URL and VS Code asks before it fetches the page.

Attached context and earlier tool results can carry into later model calls, subject to selection, caching and
compaction. Attach what the task needs and start a New Chat when the task changes. [Lab 08](../08_Analyze_Data_And_Cost/) Part D attaches a file and compares the cost.

## Names differ by setup

| Behaviour | Labels you may see |
|---|---|
| Answers or proposes an implementation approach | Ask, Plan; Plan may create a plan artifact |
| Acts, stops before most commands | Interactive, Agent |
| Acts with fewer stops | Autopilot |

The labels depend on the session target in the chat input (Copilot, Local, Cloud and others) and on your
organisation's settings. The behaviour is what matters; [Lab 00](../00_Setup_Check/) shows you which labels you
have.

For which customization file fits which repeated problem (instructions, skill, custom agent, MCP server, hook), see
[customization options](customization-options.md).

## Resources

- [AI features in VS Code cheat sheet](https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet)
- [Inline suggestions](https://code.visualstudio.com/docs/editing/ai-powered-suggestions)
- [Agent harnesses and session targets](https://code.visualstudio.com/docs/agents/run/agent-harnesses)
- [Add context to chat](https://code.visualstudio.com/docs/copilot/chat/copilot-chat-context)
- [Ask Copilot to create a pull request](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-a-pr)
  and [use Copilot code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review)
  (GitHub Docs)
