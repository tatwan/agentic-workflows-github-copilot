# Lab 02: How to plan, build and review a change

## Goal

Add a CSV export to a small Python report with Copilot: ask for a plan first, fix the plan where it is vague, let
the agent build the change and run the tests, then review the diff and the file it wrote. Finance needs revenue
written as `2085.70`, and a test that compares numbers passes for `2085.7` too, because they are the same number.
Tests check what someone decided they should check. The plan is where you make that decision.

## What you will learn

- Ask Copilot for a plan before any file changes, and read the plan for what it leaves vague.
- Edit a plan step so the tests check what the person asking for the change needs.
- Follow the agent as it edits files and runs the tests, and approve its commands.
- Review the diff and the output file yourself, and tell a passing test from a met request.

## Before you start

You need VS Code with GitHub Copilot signed in ([Lab 00](../00_Setup_Check/) checks this) and Python 3.10 or
newer. No packages: the project uses only what ships with Python. You will read some Python but not write any;
Copilot writes the code and runs it.

1. In VS Code choose **File > Open Folder** and open the `project` folder inside this lab
   (`02_Plan_Then_Build/project`). Keep this README open somewhere else, for example on GitHub, so Copilot works on
   the report and not on the lab text.
2. If VS Code asks whether you trust the authors of the folder, choose to trust it.
3. Open the Chat view and start a **New Chat**.

The project is a small report on an orders file:

| File | What it is |
|---|---|
| `orders/report.py` | `load_orders` reads the file; `monthly_summary` returns one row per month |
| `tests/test_report.py` | Five tests for the report |
| `data/orders.csv` | 97 order lines, January to June 2026 (synthetic) |
| `README.md` | What the report does and how to run its tests: `python -m unittest` |

To start over at any point, hover over your first request in the chat and select **Restore Checkpoint**, or copy
the `project` folder again from the repository.

## Part A: Decide what done looks like

Before the agent does anything, work out the right result yourself, so you can judge the agent's.

The job comes from finance: *"Can the monthly report give us a CSV we can load into our spreadsheet? One row per
month: month, orders, units, revenue. Our import expects money with two decimals."*

1. Open `orders/report.py` and read `monthly_summary`. An order can have several lines, so `orders` counts
   distinct order IDs. Revenue is a `Decimal`, which keeps money exact.
2. Open `tests/test_report.py`. The last test says January has 8 orders, 174 units and revenue `2085.70`.
3. Write down the first two lines the CSV file should have:

   ```text
   month,orders,units,revenue
   2026-01,8,174,2085.70
   ```

4. Predict: in Python, `Decimal("2085.7") == Decimal("2085.70")` is `True`. Which kind of test would notice if the
   file said `2085.7`: one that reads the revenue back as a number, or one that compares the line as text?

Checkpoint: you can write the January line exactly, and you know that only a test comparing the text of the line
catches a missing zero.

## Part B: Ask for a plan and edit it

A plan lists the files the agent will change, the steps and how it will check the work. A vague step is cheaper to
fix in the plan than in the code.

1. In the chat's mode picker choose **Plan**.
2. Paste this request:

   ```text
   Add CSV export via python -m orders.report --output FILE, with month, orders, units and revenue.
   Reuse monthly_summary and only the Python standard library.
   Keep tests/test_report.py and data/orders.csv unchanged; put new tests in tests/test_export.py.
   Plan first; do not change project files yet.
   ```

   The request leaves out the two decimals on purpose: real requests often miss something, and the plan is where
   you catch it.

3. Expand the steps: it reads the report, tests and project README. The command-line interface is part of
   your request. If it proposes only an importable function, ask it to include the requested command too.
   Keep the original tests unchanged; a separate file makes the new checks easy to review.
4. When the plan is ready, a **Review Plan** card appears. Select **Open Full Plan** to open the plan in the editor.
   Read it for three things:
   - **Files:** `orders/report.py` and a new test file. `tests/test_report.py` should not be on the list.
   - **Revenue:** does the plan say how revenue is written to the file?
   - **Tests:** what do the new tests check? Does any test read the written file as text?
5. Edit the plan. Add these lines to its steps (or change its test step to say this), then save the file:

   ```text
   Format revenue with exactly two decimals.
   Test the exported January line as text: 2026-01,8,174,2085.70.
   Also export a new one-order case worth Decimal("1.0") and one worth Decimal("1").
   Both must end in ,1.00; checking only already-two-decimal inputs misses this requirement.
   ```

   If two decimals are already in the plan, check that it includes the new one-decimal and integer cases.
   `str(Decimal("1.0"))` remains `1.0`: exact arithmetic alone does not choose a display format.

Checkpoint: the plan changes `orders/report.py`, adds a new test file, leaves the five existing tests alone, says
two decimals and includes text tests on the real January line and new one-decimal/integer inputs.

## Part C: Let the agent build and run the tests

Now the agent does the work, and it checks the work with the tests.

1. On the Review Plan card select **Implement Plan**.
2. Watch the steps. The agent repeats the cycle from Lab 01: it **looks** at the files, **acts** by editing
   `orders/report.py` and creating the test file, and **checks** by running `python -m unittest`. VS Code asks you
   before it runs a command. Read the command first: this one runs the tests and does not edit your code, so allow it.
3. Read the result in the chat or terminal. A successful run ends with the test count and `OK`, for example:

   ```text
   Ran 9 tests in 0.012s

   OK
   ```

   This is an example output. Your count is the five existing tests plus the new tests the agent wrote. If a test fails, the agent normally
   reads the failure, changes the code and runs the tests again.
4. If the agent did not run the export, ask it:

   ```text
   Run the export on data/orders.csv and save it as monthly.csv in this folder.
   ```

Checkpoint: every test passes, including the five that were there before, and `monthly.csv` is in the project
folder.

## Part D: Review the diff and the file

The tests are green. Whether finance's request is met is your decision.

1. Select **View All File Changes** in the chat (or open each changed file from the list in the chat). In the diff
   of `orders/report.py`, check:
   - The export calls `monthly_summary` instead of adding up the orders again.
   - The line that writes revenue formats it with two decimals, for example `f"{revenue:.2f}"` or
     `quantize(Decimal("0.01"))`. A conversion to `float`, as in `round(float(revenue), 2)`, drops the zero.
   - `tests/test_report.py` is not in the list of changed files.
2. Open `tests/test_export.py`. Find the real January-line check and the small cases using `Decimal("1.0")`
   and `Decimal("1")`. Both must assert `1.00` in the written CSV text. A test that starts from `1.00` alone
   can pass when the exporter merely calls `str` on a Decimal. Confirm the original test file is unchanged.
3. Open `monthly.csv`. It has seven lines: the header and one row per month.

   | month | orders | units | revenue |
   |---|---:|---:|---:|
   | 2026-01 | 8 | 174 | 2085.70 |
   | 2026-02 | 8 | 193 | 5154.25 |
   | 2026-03 | 15 | 315 | 5278.10 |
   | 2026-04 | 5 | 76 | 761.55 |
   | 2026-05 | 6 | 179 | 3087.50 |
   | 2026-06 | 6 | 126 | 1186.30 |

   Three rows end in zero: January, March and May. Those are the rows where a missing zero would show.
4. Compare with a build where nobody edited the plan, in this lab's
   [resources/without-the-plan-edit](resources/without-the-plan-edit/) folder. Its seven tests pass, and its file
   says `2085.7`, `5278.1` and `3087.5`. Its January test compares `float(revenue)` with `2085.70`, which is true
   for both. We wrote that example for this lab; your agent may or may not make the same choice.

Checkpoint: your file has seven lines, every revenue has two decimals, and you can point at the test that would
fail if a zero went missing. If something is wrong, tell the agent what you found, or restore the checkpoint.

## If your run looks different

| What you see | What to do |
|---|---|
| The mode picker shows **Ask** and **Agent** instead of **Interactive** | You are in a Local session. Plan works the same; to build, select **Start Implementation** instead of **Implement Plan** |
| There is no **Open Full Plan** | Type the four lines from Part B, step 5 into the card's feedback box and select **Submit Feedback**, or send them as a message. Wait for the revised plan |
| `python` is not found | On macOS/Linux try `python3 -m unittest` and `python3 -m orders.report --output monthly.csv`. On Windows the command is often `py -m unittest`. Tell the agent which command works, or install Python 3.10 or newer |
| `ModuleNotFoundError: No module named 'orders'`, or `NO TESTS RAN` | The tests ran from the wrong folder. Ask: `Run the tests from the project folder with python -m unittest` |
| The agent changed `tests/test_report.py` | Restore the checkpoint and add to the plan: `Do not change the existing tests` |
| Your file already says `2085.70`, but no test checks the text | The code is right today. Without the test, a later change can drop the zero and every test stays green. Ask the agent to add the test |

## What you can do now

- Ask for a plan first and read it for files, behaviour and tests.
- Edit a plan step so the tests check what the person asking needs: here, the January line as text.
- Follow the agent's look, act and check steps, and approve a command after reading it.
- Review the diff and the file yourself, and explain why `2085.7` passes a number test and fails the request.

## Challenge

1. **The same request without the edit.** Copy a fresh `project` folder, open it, start a New Chat and send the
   Part B request in Plan mode, then select **Implement Plan** without editing. Open the new tests: would any of
   them fail if a revenue lost its final zero? Expected: it varies from run to run, and you find out by reading the
   test, not from the green result.
2. **Protect the input file.** Plan a second change the same way: the export must refuse to write over
   `data/orders.csv`. Check that the plan tests the orders file stays unchanged, implement it, then ask the agent
   to try `python -m orders.report --output data/orders.csv`. Expected: an error message (for
   example `--output must not be the input file`), and `data/orders.csv` still ends at line 98 (press Ctrl+End,
   or Cmd+Down on a Mac). ⚠️ Do not try that command before the guard exists: the export reads the orders file and
   then writes the summary over it. If that happens, copy `project` again.

Answers to compare with when you finish, for the lab and the challenge: [`solved/`](solved/).

## Going further

- **Implement with Autopilot.** The Review Plan card also offers to build with fewer pauses for your approval. Use
  it when the plan has a test you trust.
- **Keep a plan.** **Approve Plan Only** approves without building. Save a copy of the plan and attach it to a new
  chat to build it later, or to hand it to a teammate.
- **Another language.** The same loop works on any project with tests, for example a Java service tested with
  `./mvnw test`: in the plan, ask for a test of exactly what the person asking will look at.
- **A pull request summary.** If you work in a Git repository, ask the agent for a summary of the change for the
  pull request, then read it against **View All File Changes**. The summary says what the agent meant to do; the
  diff shows what it did. Check that every file in the diff is in the summary, and that the summary claims no test
  you did not see pass.
- **Hand the next change to the cloud agent.** For a change like the input guard in the challenge, on a repository
  on GitHub: write an issue that states the check (`--output data/orders.csv stops with an error and leaves the file
  unchanged`), then assign it to Copilot, or choose the **Cloud** session target in the chat input. It works on GitHub and opens a
  pull request; you review that as you reviewed this diff. Your organisation decides whether the cloud agent is on.
- **A second reviewer.** On that pull request, request a review from Copilot. Its comments are one more check;
  your own review of the diff and the file is still the one that counts.
- **Cost.** Open Copilot's usage view and read what this task cost. Lab 08 compares requests by cost.

## Resources

- [Plan before you build](https://code.visualstudio.com/docs/agents/run/planning)
- [Review the agent's edits and use checkpoints](https://code.visualstudio.com/docs/agents/run/review-code-edits)
- [Ask Copilot to create a pull request](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-a-pr)
  and [use Copilot code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review)
  (GitHub Docs)
- [Which way of working](../guides/which-mode-when.md): Plan, Interactive, Autopilot, the cloud agent and the rest
- [Python `unittest`](https://docs.python.org/3/library/unittest.html)
- [Python `csv`](https://docs.python.org/3/library/csv.html) and [`decimal`](https://docs.python.org/3/library/decimal.html)
