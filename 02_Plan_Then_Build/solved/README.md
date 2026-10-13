# Lab 02: answers

Use these after you finish the lab, to compare with your own result. Copilot's wording and code change from run
to run, so compare the facts listed here, not the text. The files were written by hand to show a correct result;
they are not a saved Copilot chat.

- `project/`: the project after Parts B to D. `orders/report.py` adds `export_monthly_csv` and a command
  (`python -m orders.report --output monthly.csv`, with an optional `--input`). `tests/test_export.py` adds four
  tests, one of which compares the January line as text. `python -m unittest`: 9 tests, OK. The export writes 7
  lines with revenue to two decimals: 2085.70, 5154.25, 5278.10, 761.55, 3087.50, 1186.30 (total 17553.40).
- `challenge/project/`: Challenge 2. The command refuses an `--output` that is the same file as `--input`, with
  `error: --output must not be the input file` (exit code 2), and one more test covers it. 10 tests, OK;
  `data/orders.csv` keeps its 98 lines.
- Why the guard matters: without it, `--output data/orders.csv` replaces the orders file with the summary, because
  `load_orders` reads the whole file before the export opens it for writing.

Your agent's function and test names will differ. The export is right when the tests pass and the January line
reads `2026-01,...,2085.70`, with two decimals.
