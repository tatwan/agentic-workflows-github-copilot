# Monthly revenue export

`revenue.py` has two public functions: `csv_text(rows)` returns CSV text; `write_csv(rows, path)` writes it.
Each input row is a `(month, Decimal revenue)` pair. Keep row order and the `month,revenue` header.
Revenue must display exactly two decimal places. Inputs are already calculated; do not change amounts or inputs.

Run from this folder: `python -m unittest -v` (or `python3` / `py` for your installation).
There are four starting tests. No packages, keys, database or network connection are needed to run them.
