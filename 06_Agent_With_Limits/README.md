# Lab 06: How to build an agent that can only do its job

## Goal

Make a reviewer agent whose only tools read and search files. Ask it to review a release check, then to fix the
bug it found. It cannot: it has no tool that edits a file, whatever the request says. Then give the fix to the
normal agent, which edits files freely but stops and asks you before it runs a command. An agent's tools decide what
it can do at all; approvals decide what it must ask you first.

## What you will learn

- Write a custom agent in `.github/agents/` with a name, a description, a tool list and instructions.
- Select the agent in the chat and check from the files, not from its reply, what it changed.
- Tell a limit set by an agent's tools from a request written in a prompt or a rule.
- Read a command before you approve it, choose how long your approval lasts, and skip a command.

## Before you start

You need VS Code with GitHub Copilot signed in ([Lab 00](../00_Setup_Check/) checks this). Nothing to install, and
no coding. Python 3.10 or newer is optional: with it, Copilot can run the tests in Part C; without it, you skip that
command and read our run instead.

1. If you cloned this repository with Git, first copy this lab's `project` folder outside the repository and use
   the copy: inside a clone, Copilot may look for agents at the top of the repository and miss yours. A ZIP download
   needs no copy.
2. In VS Code choose **File > Open Folder** and open the `project` folder (`06_Agent_With_Limits/project`). Keep
   this README open elsewhere, for example on GitHub, so Copilot works on the team's files, not the lab text.
3. If VS Code asks whether you trust the folder's authors, trust it.
4. Open the Chat view.

The project is a platform team's release check:

| File | What it is |
|---|---|
| `docs/release-check.md` | The team's rule: when an endpoint counts as too slow |
| `data/before.csv`, `data/after.csv` | The p95 time of each endpoint, in milliseconds, for the last release and for the change |
| `latency_check.py` | The check: compares the two files and decides whether the release goes ahead |
| `tests/test_latency_check.py` | Five tests for the check |

An endpoint is one address of the team's web service, such as `GET /orders`. Its p95 time is the time within which
95 of every 100 requests finish.

To start over, hover over your first request in the chat and select **Restore Checkpoint**, or copy `project`
again from the repository.

## Part A: Find out why the release was stopped

This morning the check stopped the release. Decide yourself whether it was right, so you can judge the review.

```text
GET /orders            200   220  +10.0%  too slow
GET /orders/{id}       120   126   +5.0%  ok
POST /orders           400   416   +4.0%  ok
GET /customers         150   141   -6.0%  ok
GET /reports/monthly   800   872   +9.0%  ok
DELETE /orders/{id}     90    90   +0.0%  ok
GET /exports             -   310          new
Release blocked: GET /orders too slow.
```

1. Open `docs/release-check.md` and read the first rule.
2. Open `data/before.csv` and `data/after.csv`. `GET /orders` went from 200 to 220 milliseconds: 20 more out of
   200, which is 10%.
3. Open `latency_check.py` and go to line 27 (**Go > Go to Line/Column**), inside `is_too_slow`. `>=` means "10%
   or more".

Checkpoint: `GET /orders` is exactly 10% slower, and the rule says exactly 10% is still within the limit. The check
uses `>=`, so it counts exactly 10% as too slow. A bug in the check stopped the release, not a slow endpoint. None
of the five tests tries exactly 10%, so they all pass.

## Part B: Make a reviewer that can only read

A custom agent is a Markdown file in `.github/agents/`. It names an agent, says what the agent is for, lists the
tools it may use and gives it instructions. The tool list is what this lab is about: an agent cannot use a tool that
is not on its list.

1. In the Explorer, select **New File...** and type the whole path, `.github/agents/reviewer.agent.md`. Paste this
   and save:

   ```markdown
   ---
   name: reviewer
   description: Reviews code against the team's rules in docs/ and reports each problem with its file and line.
   tools: ['read', 'search']
   ---
   You review code for the team. Read the files you are asked about and the team's rules in docs/.
   For each problem, give the file and line, what is wrong and the change you suggest.
   You have no tools to edit files or run commands. If you are asked to, say so and leave the change to the person.
   ```

   The header sits between the two `---` lines. `name` is what the agent picker shows; `description` says what the
   agent is for; `tools` lists two tool sets, `read` (open files) and `search` (find files and text). There is no
   `edit` and no `execute` (the terminal). Below the header are the instructions sent with every request.
2. Start a **New Chat**. Open the picker where you choose Interactive or Plan and select **reviewer**.
3. Paste:

   ```text
   The release check blocked today's release because of GET /orders.
   Review latency_check.py against docs/release-check.md. Is the check right?
   ```

4. Expand the steps: the agent reads the rule, the code and perhaps the data, and searches. Nothing else.

Checkpoint: the review names `is_too_slow` and its `>=` on line 27, says exactly 10% is within the limit, and
suggests `>`. It may add that no test tries exactly 10%. If your review looks different, compare it with
[resources/examples/review.md](resources/examples/review.md), an example we wrote.

Now predict: what will the reviewer do if you ask it to fix the bug?

5. In the same chat, paste:

   ```text
   Good catch. Fix it now and run the tests.
   ```

Checkpoint: check the files, not the reply.

- `latency_check.py` still has `>=` on line 27.
- No **Keep** or **Undo** buttons appear in the editor, and the chat lists no changed files.
- The steps show no edit and no terminal command.

The reply usually says the agent cannot edit or run anything and shows the change for you to make. A reply can say
anything, which is why you check the file. The last line of the instructions only tells the agent how to answer;
what stops it is the `tools` line. In [Lab 04](../04_Team_Rules/) a rule said "run no commands": a rule asks the
model, while a missing tool cannot be used.

## Part C: Let the normal agent fix it, with your approval

The normal agent has all the tools. It edits files in this folder without asking, and you review the edits with
Keep and Undo. Commands are different: with **Manual permissions**, the default, it stops before most commands and
waits for your answer.

1. Start a **New Chat**. In the picker choose **Interactive** (on a Local session, **Agent**).
2. Paste:

   ```text
   In latency_check.py, is_too_slow flags exactly 10%, but docs/release-check.md allows it.
   Change >= to >, add a test for exactly 10%, then run the tests.
   ```

3. Watch the steps. The edits appear in the editor with Keep and Undo: `>` on line 27, and a new test in
   `tests/test_latency_check.py`. Nobody asked you about those.
4. Then the chat stops and shows a command, usually `python -m unittest`. Before you answer, read it: what does it
   run, in which folder, and could it change or delete a file? This one runs the tests and changes no code or data.
   - If you have Python: select **Allow**. The arrow next to it sets how long your answer lasts: this once, this
     session, this workspace, or always. Choose the narrowest one, **Allow Once**.
   - If you do not have Python: select **Skip**.
5. Read the agent's last message, then select **Keep** on both files.

Checkpoint, if you allowed: the output ends `Ran 6 tests` and `OK`, the five old tests plus the new one. If you
skipped: the agent says the tests were not run, and does not say they passed. Our run of the same tests and the check
is in [resources/after-the-fix/output.txt](resources/after-the-fix/output.txt): 6 tests OK, and `Release can go
ahead: no endpoint is too slow.` Either way, line 27 now reads `>`.

| Control | Decides | Where you set it |
|---|---|---|
| The agent's `tools` list | What the agent can do at all | The `.agent.md` file |
| Approvals | Which actions wait for you | The approval prompt, and the permissions menu in the chat input |

Under **Manual permissions** some read-only commands, such as listing a folder, run without asking; **Allow all**
and Autopilot mode run everything without asking. **Chat: Reset Tool Confirmations** in the Command Palette clears
approvals you gave for longer than once.

## If your run looks different

| What you see | What to do |
|---|---|
| **reviewer** is not in the agent picker | Check the path: `.github/agents/reviewer.agent.md`, directly inside the folder you opened, with the name ending in `.agent.md`. Run **Developer: Reload Window**. If you cloned the repository, copy `project` outside it (Before you start, step 1) |
| The reviewer changed a file | Check which agent the picker shows: Interactive was probably selected. Select **Undo**, choose **reviewer** in a New Chat and repeat Part B |
| The agent did not ask before running the tests | Check the actual permission setting and any earlier approvals. Some read-only commands run without a prompt even with Manual permissions; inspect the steps rather than assuming every command must ask |
| `python` is not found, or `No module named latency_check` | On Windows try `py -m unittest`; on macOS/Linux try `python3 -m unittest`. Run from the `project` folder |
| The skipped agent says the tests pass | It did not run them. Ask: `Did you run the tests?` |

## What you can do now

- Write a custom agent in `.github/agents/` with a name, a description, a tool list and instructions.
- Check what an agent changed from the files, the Keep and Undo marks and the steps, not from its reply.
- Explain why a reviewer without an `edit` tool cannot fix code, while a rule only asks.
- Read a command before you approve it, allow it once or skip it, and find where approvals are set.

## Challenge

1. **An agent that runs but does not edit.** In a fresh copy of `project`, add
   `.github/agents/test-runner.agent.md` with `tools: ['read', 'search', 'execute']` and the instruction to run the
   tests and report what they print. Ask it to run the tests, then to change `>=` to `>`. Expected: the command may wait for approval, and the starting tests pass (5 tests). With no edit tool, it either says it cannot edit or proposes a terminal command
   that rewrites the file: skip that one. A command can change files, so `execute` is broad and your approval is the
   control left.
2. **A reviewer that saves its review.** Ask the reviewer: `Write your review to reviews/latency.md.` Expected: no
   file appears; the review stays in the chat. Then decide how the reviewer could save reviews without touching the
   code. A tool list cannot limit `edit` to one folder, so adding `edit` lets it change `latency_check.py` too.
   Either save the review yourself, or add `edit` with a rule like Lab 04's and review every change with Keep and
   Undo.

Answers to compare with when you finish, for the lab and the challenge: [`solved/`](solved/).

## Going further

- **A performance report.** With Python, ask the normal agent:
  `Run latency_check.py on data/before.csv and data/after.csv and write report.md:`
  `a table of every endpoint with before, after, change and status, and a one-line verdict.`
  Approve the command once, then check one row by hand, for example `GET /reports/monthly`: 800 to 872 is +9.0%,
  `ok`. `GET /exports` should be `new`, with no change.
- **More header fields.** `handoffs` adds a button after the answer that switches to another agent with a prepared
  prompt, such as "Apply this fix"; `model` picks the agent's model.
- **Approve one command in advance** with the setting `chat.tools.terminal.autoApprove`, for example
  `python -m unittest`. VS Code's documentation calls terminal auto-approval a convenience, not a security boundary.
- **Agents for you alone** go in `~/.copilot/agents` and are available in every folder you open.

## Resources

- [Custom agents in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents): file locations,
  header fields, handoffs
- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) (GitHub
  Docs): tool names such as `read`, `search`, `edit` and `execute`
- [Approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals): permission levels and terminal
  auto-approval
- [Use tools in chat](https://code.visualstudio.com/docs/agents/run/tools)
- [Back to the labs](../README.md)
