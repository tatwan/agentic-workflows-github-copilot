# Lab 00: How to check that VS Code, Copilot and the project are ready

## Goal

Confirm that your editor and Copilot seat offer the features you need, and that the project's checks pass before
an agent changes anything. A missing role or an unavailable feature becomes a setup finding you can act on here.

## What you will learn

- Open the project folder and check which instructions Copilot discovered.
- Distinguish the harness, its interaction mode, and its permission level.
- Record available features and identify questions for your Copilot administrator.
- Run the Python, Java, SQL and dbt baselines with uv and the Maven Wrapper.
- Find monthly credit usage and the token and credit details for a chat response.

## Before you start

Use VS Code 1.141 or later with GitHub Copilot signed in, Git, [uv](https://docs.astral.sh/uv/getting-started/installation/),
and a [Java 21 JDK](https://adoptium.net/temurin/releases/?version=21). Python 3.13.15 is selected by the project's
`.python-version`; uv can install it if necessary. The Maven Wrapper downloads Maven 3.9.16 on its first run.
You need network access to the Python package index, Maven Central and Copilot. No API key or `.env` is required.

Open `orders-analytics/` as the VS Code folder. Read [GUIDE.md](GUIDE.md) in a separate viewer so the lab guide is
outside the agent's working folder. Folder choice narrows normal context; it does not prevent an agent from
reading other folders through its tools. Review the files it reads.

Runtime: your machine, CPU. Supports D01 setup and agent controls (33–39), skills and CLI access (94, 99, 119),
organisation controls (140), and usage (176). Synthetic project data is reused from the October 6 repository
build under the repository's [MIT licence](../LICENSE); no client data is used.

## What you will do

**Part A: Open the project and check your account.** Record the editor version and Copilot plan; confirm Source
Control finds the parent repository.

**Part B: Check the harness and modes.** Select Copilot and record the modes it offers, with Manual permissions.

**Part C: Record feature availability.** Check models, skills, hooks and the optional CLI; distinguish an
unavailable feature from a confirmed policy restriction.

**Part D: Run the project checks.** Sync the locked environment and establish four passing baselines.

**Part E: Read a file with Copilot and inspect usage.** Send one bounded question, inspect its file reads, check
its answer yourself, and record credits.

**Challenge.** Complete your environment record and decide which lab prerequisites you can meet.

## Checkpoints

| After | What to check | Our run on 11 Oct 2026 |
|---|---|---|
| A | Project folder visible; parent repository in Source Control; plan recorded | `orders-analytics/`, parent repo on `main`; VS Code 1.141.0; Copilot Student |
| B | Harness, modes and permissions recorded | Copilot; Interactive, Plan, Autopilot; Manual; no built-in Ask role |
| C | Features recorded as available, unavailable or not tested | `/skills` listed 30 skills; Hooks editor available; CLI absent locally; Free seat and Codespaces not tested successfully |
| D | All four baselines pass | Python 5 passed; Java 5 tests, no failures or errors; customers 300, orders 100,000, line items 249,285, complete orders 85,045; dbt PASS=17 |
| E | File-reading tools, correct function name, no project edits, usage recorded | All three fresh chats found the existing revenue test using two file reads each; response costs 2.4, 0.3, 0.3 credits |

The baselines passed in a fresh copy and on the working project with Python 3.13.15 and Temurin JDK 21.0.12.1.
Copilot output and cost vary. Parts A–D used no AI credits. Part E needs one response: our measured range was
0.3–2.4 credits, with 3.0 credits across three verification runs. Use your own displayed cost, not that range as a
budget guarantee. The optional worked challenge used 1.7 credits in one verification run; all four model
responses in this build used 4.7 displayed credits. The run model is named once in the [repository README](../README.md).

Our Copilot Chat view did not show the documented context-window control. Response details exposed tokens and
credits, and the status dashboard showed monthly usage. The guide provides that observed route and tells you how
to record a missing control. A Codespaces route is withheld until its harness, hooks and CLI have been run there.

## Resources

- [The guide](GUIDE.md): each check, recovery steps and the challenge.
- [Environment record](resources/environment-record.md): keep your own copy outside the project folder.
- [VS Code harness controls](https://code.visualstudio.com/docs/agents/run/agent-harnesses): what each control selects.
- [VS Code credit usage](https://code.visualstudio.com/docs/agents/guides/optimize-usage): response, session and monthly usage.

[Back to the lab list](../README.md)
