# Lab 03: answers

Use these after you finish the lab, to compare with your own result. Copilot's wording and code change from run
to run, so compare the facts listed here, not the text. The files were written by hand to show a correct result;
they are not a saved Copilot chat.

- `fct_orders.sql`: the fix, `coalesce(d.discount_amount, 0)` in both columns. Your agent may write `ifnull` or a
  `case` instead. Any version is right that keeps the `left join` and the complete-order filter and gives 0 for a
  missing discount.
- `build-output.txt`: PASS=19 WARN=0 ERROR=0 TOTAL=19.
- `rows-output.txt`: 35 orders, 35 with a net amount, net total 6,417.95. Order 1: gross 267.36, discount 0, net
  267.36. Order 4: 46.55, 10, 36.55 (`dbt show` drops trailing zeros).
- Checked from the CSV files alone: 40 orders, 35 complete (Ctrl+F `,complete,` in `raw_orders.csv` finds 35), 14
  discounts, of which 3 belong to cancelled orders (22, 29 and 32), so 11 complete orders have one. Gross 6,522.95,
  discount 105.00, net 6,417.95.
- The starting project: PASS=17 ERROR=2, both `not_null_fct_orders_discount_amount` and
  `not_null_fct_orders_net_amount` with "Got 24 results". Rows: 35 orders, 11 with a net amount.
- The prepared examples in `../resources/`: the loosened tests give PASS=17 WARN=2, still 35 rows with only 11 net
  amounts; the inner join gives PASS=19 with 11 rows, and order 1 is missing.
- `challenge/assert_every_complete_order_is_kept.sql`: Challenge 2. With the fix, PASS=20 (`build-with-fix.txt`);
  with the inner join, `FAIL 24 assert_every_complete_order_is_kept` (`build-with-inner-join.txt`).
- Challenge 1 has no single answer: the loose request may give a right fix, loosened tests or dropped rows. Say which
  you got, from the changed files and the row count.
- Going further: a dbt unit test on `fct_orders` with orders 1 and 4 as given rows, expecting discount 0 and net
  267.36 for order 1, passes on the fix and fails on the starting model (`0.00` becomes `NULL`).
