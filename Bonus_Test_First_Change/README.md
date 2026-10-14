# Bonus: How to fix a bug with tests before refactoring

## Goal

Use Copilot to reproduce a small export bug before it changes the implementation. Then fix the bug and remove
one duplicated loop while keeping the tests green. The useful moment is a passing starting suite followed by a
new test that fails on a value the suite never tried. Green tests describe the cases you checked; they do not
prove every input works.

## What you will learn

- Turn a reported bug into an observable failing regression test.
- Stop the agent between writing a test, fixing code and refactoring it.
- Preserve the public interface and original tests during a small refactor.
- Save the checked sequence as a skill for the next bug.

## Before you start

This is optional developer practice. You need VS Code, GitHub Copilot and Python 3.10 or newer. There are no
packages to install. [Lab 02](../02_Plan_Then_Build/) helps with reviewing code changes; [Lab 05](../05_Make_A_Skill/)
helps with skill installation, but the steps below stand alone.

1. Open this lab's `project` folder as its own VS Code workspace, with this guide open elsewhere. If using a Git
   clone, copy `project` outside the clone first so the optional skill lives at the workspace root.
2. Open a New Chat. Choose Interactive (or Agent in a Local session), with Manual permissions. Keep the same model
   through the exercise. Read any proposed command before approving it once.
3. Open a terminal from **Terminal > New Terminal**. It must start in `project`, where `revenue.py` lives.
4. Run `python -m unittest -v`. On macOS/Linux use `python3` if needed; on Windows use `py` if needed. Use that same
   executable in later steps.

Checkpoint: four tests pass. The files are synthetic examples under the repository licence. To restart, open a
new copy of `project`. Keep completed folders and chats if you want to compare them later.

## Part A: Identify what the starting tests miss

The exporter has two entry points: `csv_text(rows)` returns text and `write_csv(rows, path)` writes a file. A row
is a month plus a `Decimal` amount, such as `("2026-01", Decimal("12.50"))`. Decimal represents the supplied amount
without introducing binary floating-point approximations. The export must display two places after the decimal.

1. Open `tests/test_revenue.py`. It checks the header, two already-formatted amounts, file/text agreement and
   unchanged input. None of those tests supplies an amount with fewer than two decimal places.
2. Open `revenue.py`. Both functions turn the amount into text with `str(revenue)`.
3. Predict what `Decimal("1.0")` and `Decimal("1")` will look like in the CSV. Both mean one unit of revenue,
   but the display contract calls for `1.00` in both cases.
4. Ask Copilot for a diagnosis without a repair:

   ```text
   Read revenue.py and tests/test_revenue.py. Explain why all four tests can pass
   while an amount Decimal("1.0") is exported with the wrong number of decimal places.
   Leave all files unchanged; name the two public export paths that need the same behavior.
   ```

Checkpoint: it identifies both functions and the gap in the test inputs. Check the files remain unchanged. A
plausible explanation is useful, but the next part turns it into something executable.

## Part B: Add the failing test and stop

A **regression test** captures a bug so a later change can detect it again. In test-driven development, the
failing-test stage is called **red**, a passing implementation **green**, and cleanup that preserves behavior
**refactoring**. The stop between stages lets you inspect what is being proved.

1. Send:

   ```text
   Add tests/test_money_display.py for csv_text and write_csv using Decimal("1.0") and Decimal("1").
   Both must export 2026-03,1.00. Keep revenue.py and tests/test_revenue.py unchanged.
   Run python -m unittest -v and stop after showing why the new tests fail; do not fix production code yet.
   ```

2. Inspect the diff before going further. Only the new test file should have appeared. If the agent repaired
   `revenue.py` already, undo that production edit, keep the new tests and rerun them.
3. Read the actual test output. An assertion should compare `2026-03,1.0` or `2026-03,1` with `2026-03,1.00`.
   A syntax error, failed import or test that was never discovered does not reproduce the bug.
4. If you need a comparison, open [the prepared regression](resources/red/test_money_display.py) outside the
   workspace. Copy it into `tests/` only if your test needs replacing, then run the suite again.

Checkpoint: the original four tests still pass, and the new assertions fail for the missing decimal places.
The prepared version runs six test methods and reports four failing subtests. Your agent may organize the tests
differently; judge the failing inputs and both export paths, not the exact test count.

## Part C: Make the smallest fix

Now authorize the implementation. A correct fix should satisfy the display contract without changing the input
amount, public function names, header or row order.

1. Send:

   ```text
   Make the smallest change in revenue.py so both export paths always display two decimal places.
   Preserve all tests, public functions, row order and header. Add no dependencies.
   Run the full suite and report the actual result, then stop before refactoring.
   ```

2. Inspect the diff. A change from `str(revenue)` to a two-decimal format is enough for this bug. An agent that
   deletes the regression, changes `1.00` to `1.0`, or skips it has weakened the evidence.
3. Run the suite yourself in the terminal. If the agent could not run Python, its code can still be reviewed;
   mark its execution as not run and use your own output.

Checkpoint: all original and new tests pass. Both one-unit inputs produce `1.00` in the returned text and file.
[resources/green/revenue.py](resources/green/revenue.py) is a prepared minimal fix with the repeated loop still
present. It separates the behavior change from the cleanup that follows.

## Part D: Refactor under the passing tests

The duplicated loop now contains the same money rule twice. Sharing it gives a future rule change one place to
edit. Keep the two public entry points because callers may use either one.

1. Send:

   ```text
   Refactor only revenue.py to share the CSV-writing loop between csv_text and write_csv.
   Keep their names, signatures, output and all tests unchanged. Use a small private helper; add no modules.
   Run the full suite and explain what duplication you removed.
   ```

2. Review the helper. It should write the header and formatted rows to the supplied output stream. File opening
   still belongs to `write_csv`; returning the string still belongs to `csv_text`.
3. Rerun the suite and compare the diff with the earlier green stage. The tests should not change at this stage.

Checkpoint: the same cases pass before and after the cleanup, with one shared writing loop. A passing suite
supports the covered behaviors; review any other changes separately. There is no reason to add services,
interfaces or a new package for this small exporter.

## If your run looks different

| What you see | What to do |
|---|---|
| No tests were discovered | Run from `project`, and keep `tests/__init__.py` |
| The new failure is an import error | Fix the test import before treating it as red; the bug must fail an assertion |
| Copilot edits production code in Part B | Undo only that edit, keep the regression and rerun before approving Part C |
| The tests pass after expected values were weakened | Restore the `1.00` assertions and original tests, then repair the exporter |
| A command waits for permission | Read it; approve once if it is the local test command, or run it yourself |

## What you can do now

- Demonstrate a bug with an assertion that fails for the intended reason.
- Review each stage before allowing the next one.
- Remove duplication while retaining the same public behavior and regression tests.
- Reuse the sequence through a reviewed skill, with human stop points.

## Challenge

1. Add a new test file for `Decimal("0")` and `Decimal("-2.5")` in both export paths. Expected rows end in
   `0.00` and `-2.50`, in input order. Check the input list stays unchanged and empty input writes only the header.
   The existing fix should already pass; a useful new regression need not always fail.
2. Copy [resources/test-first-change](resources/test-first-change/) into `.github/skills/` inside your project.
   Read its steps, reload the window if needed and start a New Chat. Select `/test-first-change` from the command
   list and ask it to check an amount `Decimal("2.5")` displays as `2.50`. It should run the baseline, add a test,
   see that it already passes and explain that no new failing bug was reproduced. It should not invent a bug or
   make an unnecessary production change. Check discovery, invocation and test output separately.

Answers for the core and challenge: [`solved/`](solved/). All supplied answers are prepared examples.

## Going further

Use the skill for a different reported bug with an explicit expected value. Keep each change small enough to
review. For a larger refactor, first add tests around the externally visible behavior, then move one part at a
time. The tests support review; they do not remove the need for it.

## Resources

- [Test-driven development in VS Code](https://code.visualstudio.com/docs/agents/guides/test-driven-development-guide)
- [Refactor safely with agents](https://code.visualstudio.com/docs/agents/guides/refactor-safely)
- [unittest](https://docs.python.org/3/library/unittest.html) and [decimal](https://docs.python.org/3/library/decimal.html)
- [Agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
