# Bonus: answers

Use these after you finish the lab, to compare with your own result. Copilot's wording and code change from run
to run, so compare the facts listed here, not the text. The files were written by hand to show a correct result;
they are not a saved Copilot chat.

- `start-output.txt`: building the database (300 customers, 100,000 orders, 249,285 line items; 85,045 complete
  orders) and the original query's first ten rows. Customer 1 starts with orders 50492 and 97958 on 2025-01-01, both
  at 2575.26 (690.00 + 1,885.26), then 85296 on 2025-01-02 at 3350.96.
- `running_value_fast.sql`: one right rewrite. Per-order values in a CTE, then
  `sum(...) OVER (PARTITION BY customer_id ORDER BY order_date RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.
  Your agent's rewrite may differ (a window with no frame line, a join to per-day totals); any version that
  `compare_rows.py` calls `SAME ROWS` with `same order: yes` is right.
- `compare-output.txt`: 85,045 rows each, 0 and 0 different, same order yes, `SAME ROWS`. `rows-output.txt`: the
  first ten rows, identical to the original's.
- `time-output.txt`: medians of five runs after a warm-up. Times depend on your computer; on ours the original took
  about 0.45 s and the rewrite about 0.16 s.
- The prepared wrong rewrite in `../resources/rows-frame/` uses `ORDER BY order_date, order_id ROWS ...`:
  `DIFFERENT ROWS`, 25,911 rows each way (30.5%), first difference order 50492 with 690.00 against 2575.26, and as
  fast as the right rewrite. Adding `order_id` to the ORDER BY with no frame line gives the same 25,911 differences.
- `challenge/tiny_case.py` and `tiny-case-output.txt`: one answer to Challenge 2. The original and the right
  rewrite give `30.00 / 30.00 / 35.00`; the ROWS frame gives `10.00 / 30.00 / 35.00`.
- Challenge 1 has no single answer: the loose request may edit the original in place, skip the comparison or use a
  ROWS frame. Say which you got, from the changed files, the comparison and the first two rows.
