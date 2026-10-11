# Agentic Workflows with GitHub Copilot: labs

Hands-on labs for running GitHub Copilot as an agent in VS Code: hand it a task and check its work, give it your
team's rules, turn a method into a skill, build a small agent with limited tools, control what it may run, and see
what a session costs. They are written for people who use Copilot already, whether they write Java or Python, work
with SQL and dbt, lead delivery, or do not code at all. Every lab works on one small fictional codebase,
`orders-analytics/`, with synthetic data.

Product details and local behavior were checked on 11 Oct 2026 against VS Code 1.141.0. Copilot changes often, some features used here are
in preview, and your organisation may have turned some off; each lab says which.

## The labs

| Lab | What you do | Status |
|---|---|---|
| [00 Environment check](00_Environment_Check/) | Check your editor, plan and project are ready | Ready for review; access gaps recorded |
| [01 Hand Copilot a task](01_Hand_Copilot_A_Task/) | Run a task in Ask, Plan and Agent, and test the agent's tests | Planned |
| [02 Team rules](02_Team_Rules_In_Instructions/) | Write instructions files and check they loaded | Planned |
| [03 Review a slow query](03_Review_A_Slow_Query/) | Prove a query rewrite by its plan and its rows | Planned |
| [04 dbt change](04_dbt_Change_Without_Weakening_Tests/) | Fix a failing dbt test in the model, not the test | Planned |
| [05 Write a skill](05_Turn_A_Method_Into_A_Skill/) | Write a skill and test when it loads | Planned |
| [06 Custom agent](06_Custom_Agent_With_Limited_Tools/) | Build a reporting agent with only the tools it needs | Planned |
| [07 Control what runs](07_Control_What_An_Agent_Runs/) | Compare an approval rule with a hook that blocks | Planned |
| [08 Session cost](08_See_And_Lower_Session_Cost/) | Measure credits and compare runs by cost per solved task | Planned |
| [09 Work without code](09_Agent_Work_Without_Code/) | Analyse a file, sort a folder, turn notes into actions | Planned |
| [10 Check a customization](10_Check_A_Customization_Helps/) | Test whether a shared skill helps before you share it | Planned |

Learning paths: developers 00, 01, 02, 05, 07, 08 · data 00, 01, 03, 04, 05 · delivery 00, 01, 06, 10 ·
no code 00, 01, 09, 08.

## Setup

You need VS Code with GitHub Copilot signed in, Git, and [uv](https://docs.astral.sh/uv/). Labs 02 and 07 also need
a Java 21 JDK (the project's Maven Wrapper downloads Maven). Then:

1. Clone this repository.
2. Open the `orders-analytics` folder in VS Code (not the repository root), so Copilot reads its `.github/` files
   while the lab guides sit outside its normal project context. Folder choice is not an access restriction; inspect the agent’s file reads.
3. In a terminal in that folder, run `uv sync --locked`.
4. Follow [Lab 00](00_Environment_Check/).

The local route is verified. A Codespaces route is not offered yet: its Copilot harness, hooks and CLI could not be tested for this project. No devcontainer configuration is shipped.

Our three baseline read-only runs used Auto on a Copilot Student seat, which routed to `mai-code-1.1-flash`; the worked challenge used Auto and routed to `gpt-5.6-luna`. Learners use what their picker offers; availability depends on account and policy.

## How to read a lab

Each lab is a guide (`GUIDE.md`) with numbered steps, what to look for after each one, and a checkpoint table.
Copilot's answers differ from run to run, so checkpoints list facts to check, with what we saw over several runs,
never exact wording. Built labs report the AI credits their parts used in our runs. Only Lab 00 is rebuilt in this revision; the remaining folders hold planned notices and any preserved fixtures. Each one ends with a short
challenge and a list of resources.

## Project files

`orders-analytics/` holds the Python report and its tests, a Java pricing module, a seeded DuckDB database builder,
dbt seeds and models, illustrative performance files, and inbox data. All data is synthetic and authored for
these labs under the [MIT licence](LICENSE). The checked-in files are reused from the October 6 build; databases,
Python environments and Java/dbt outputs are recreated locally.

The Maven Wrapper is Apache Maven Wrapper 3.3.4 (Apache License 2.0), using the official `only-script` distribution.
Its Unix and Windows scripts are in `orders-analytics/java/`; the Python environment and lock are in the project
root. Package changes start in `pyproject.toml`; update the lock and regenerate `requirements.txt` with
`uv export --frozen --no-dev --no-emit-project --no-hashes --format requirements-txt -o requirements.txt` from
`orders-analytics/`.

The project’s `.github/` holds its conventions and later customizations. A small `.github/copilot-instructions.md`
at the parent Git root links to those conventions because the Copilot harness discovers always-on repository
instructions there. The editor may also load ancestor instructions; this folder arrangement does not isolate
an agent’s filesystem access.

No teaching branches are needed. Each later guide will specify its starting state on `main` and any fixture
copied from that lab’s `resources/`. No `.env` is needed for setup; Lab 07’s fake file is stored as `fake.env`
outside the project and is copied in only for that exercise.
