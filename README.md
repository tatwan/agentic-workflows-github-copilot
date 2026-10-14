# Agentic Workflows with GitHub Copilot: labs

Hands-on labs for working with GitHub Copilot as an agent in VS Code. You give Copilot a task, watch what it reads,
changes and runs, and check the result yourself before you trust it. The labs are for anyone with a Copilot seat:
people who write code or SQL, and people whose work is documents, folders and spreadsheets. Most of them need only
VS Code and Copilot, and no coding. Each lab has its own small project with made-up data.

Copilot changes every month. The steps were checked in October 2026 against VS Code 1.141. Some features used here
are in preview, and your organisation may have turned some of them off; [Lab 00](00_Setup_Check/) shows you how to
tell.

## The labs

| Lab | What you do | You need |
|---|---|---|
| [00 Setup check](00_Setup_Check/) | Work down a checklist: Copilot signed in, the mode picker, one file read, one command you approve | Copilot (Python and uv rows optional) |
| [01 How an agent works](01_How_An_Agent_Works/) | Ask where an old product name appears in a set of team documents, then hand over the rename and watch the agent look, act and check | Copilot |
| [02 Plan then build](02_Plan_Then_Build/) | Ask for a plan, fix the step that is vague, let the agent build a CSV export and run the tests, then review the diff and the file | Copilot + Python |
| [03 Fix a data pipeline](03_Fix_A_Data_Pipeline/) | Fix a failing dbt build without loosening its tests: say which file may change, then check the rows yourself | Copilot + uv |
| [04 Team rules](04_Team_Rules/) | Ask for the same review before and after you add your team's rules, and see a rule for review files stay out of a reply | Copilot |
| [05 Make a skill](05_Make_A_Skill/) | Turn meeting notes into actions once, save the method as a skill, run it with `/meeting-actions`, then install a teammate's skill | Copilot |
| [06 Agent with limits](06_Agent_With_Limits/) | Make a reviewer agent that can only read, ask it to fix a bug and see that it cannot, then approve the normal agent's command | Copilot (Python optional) |
| [07 Organise files and notes](07_Organize_Files_And_Notes/) | Get a plan as a table before anything moves, catch a look-alike that is not a duplicate, and approve one batch of moves | Copilot |
| [08 Analyze data and cost](08_Analyze_Data_And_Cost/) | Turn a CSV of orders into a one-page report with a chart, check one number, then compare what two requests cost | Copilot |
| [Bonus: SQL query review](Bonus_SQL_Query_Review/) | Ask for a faster version of a slow query, prove it returns the same rows, then time it | Copilot + uv |

Where to start:

- **Everyone:** 00, 01, 04, 05, 07 and 08.
- **Developers:** add 02 and 06.
- **Data and SQL work:** add 03 and the SQL bonus.

Do Lab 00 first. After that each lab stands on its own; the numbers give a sensible order, not a required one.
When you know the basics, [which way of working](guides/which-mode-when.md) puts the choices side by side: from a
suggestion as you type to an agent that opens a pull request.

## Setup

### What you need

| Setup | You need | Labs |
|---|---|---|
| Copilot only | VS Code with the GitHub Copilot extension, signed in with the account that holds your Copilot seat | 00, 01, 04, 05, 06, 07, 08 |
| + Python | Python 3.10 or newer. Nothing to install with it: these labs use only what ships with Python | 02, and the optional tests in 06 |
| + uv | [uv](https://docs.astral.sh/uv/getting-started/installation/). The first time a lab runs, it downloads dbt or DuckDB, and a Python if your computer has none | 03 and the SQL bonus |

Most people never need more than the first row. Everything runs in VS Code on your own computer; there is no
Codespaces setup.

### Get the files

1. On this repository's GitHub page, select **Code > Download ZIP** and unzip it anywhere. You do not need Git.
2. Work through [Lab 00](00_Setup_Check/). It ends with a table of the labs your setup is ready for.

If you prefer Git, clone the repository instead. For Labs 04, 05 and 06, copy the lab's `project` folder to a place
outside the clone and open the copy. Those labs add a rule file, a skill or an agent inside `project`, and inside a
clone Copilot may look for them at the top of the repository and miss them. A ZIP download needs no copy.

### Open one lab at a time

Each lab folder holds a `README.md` and a `project` folder. In VS Code choose **File > Open Folder** and open the
lab's `project` folder, not the lab folder or the whole repository. Read the README somewhere else, for example on
GitHub in your browser. Copilot then works on the lab's files, and the lab text and the prepared examples next to
`project` are not part of what it searches.

If VS Code asks whether you trust the authors of the folder, trust it: Copilot's agent features are off in a folder
you have not trusted.

Every Copilot request uses part of your monthly allowance of AI credits. A lab sends a handful of short requests.
[Lab 08](08_Analyze_Data_And_Cost/) shows where to see what a task cost.

## How to read a lab

Every lab README has the same shape.

- **Goal:** what you will be able to do, and the moment in the lab that shows it. **What you will learn** lists four
  abilities; **What you can do now**, near the end, answers the same list.
- **Before you start:** what to open, what the project holds, and how to start over.
- **Parts A to D** (Lab 05 adds E): Part A usually has you work out the right answer yourself, before Copilot
  starts, so you have something to check its work against. Each later step gives a short request to paste into the
  chat, then what to look for in the reply and a checkpoint.
- **If your run looks different:** what to do when Copilot takes another route.
- **Challenge**, then **Going further** (optional ideas) and **Resources**.
- **`solved/`**, next to the README: the answers to the lab and the challenge. Open it when you have finished,
  not before: the lab teaches by having you check Copilot's work against what you worked out yourself.

Copilot's replies change from run to run, so checkpoints list facts to check, such as a number, a file name or
whether a file changed, never exact wording. Some lessons depend on Copilot making a mistake it may not make on your
run. For each of those, the lab's `resources/` folder holds a prepared example of the mistake, and the README tells
you when to open it.

You do not write code. Where something runs, Copilot proposes the command, you read it and allow it, and the README
says what the result means. The labs call the read-only mode **Plan** and the mode that acts **Interactive**; some
setups show **Ask** and **Agent** instead.

To start over, hover over your first request in the chat and select **Restore Checkpoint**, or copy the `project`
folder again from the ZIP or your clone. Lab 07 is the exception: Copilot moves files with terminal commands, which a
checkpoint does not undo, so there you copy the folder again.

## Project files

| Folder | What it holds |
|---|---|
| `NN_Lab_Name/project/` | The lab's starting files: the folder you open in VS Code |
| `NN_Lab_Name/resources/` | Prepared examples, and files a lab asks you to copy in |
| `NN_Lab_Name/solved/` | The answers: a finished `project/` or the expected results, and the challenge answers |
| [`examples/`](examples/) | Short customization files to adapt for your own repository: file-type instructions, a skill and a read-only agent |
| [`guides/`](guides/) | Three reference pages: [which way of working fits which task](guides/which-mode-when.md), [which customization file fits which problem](guides/customization-options.md) and [how AI credits are counted](guides/saving-tokens.md) |

All data is synthetic, written for these labs, and shared under the [MIT licence](LICENSE).

The two uv labs pin their packages in `pyproject.toml` and `uv.lock` inside `project/`, so every computer gets the
same versions: dbt-core 1.12.5 with dbt-duckdb 1.11.0 in Lab 03, and DuckDB 1.5.6 in both. What they create while
they run (`.venv/`, `orders.duckdb`, dbt's `target/` and `logs/`) stays in your copy and is ignored by Git.
