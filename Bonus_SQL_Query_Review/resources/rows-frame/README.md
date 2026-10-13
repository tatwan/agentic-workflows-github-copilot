# A rewrite that is fast and wrong

This query returns as many rows as the original, in the same order, about three times faster. We wrote it for this
lab; it is not a recorded Copilot run.

| File | What it is |
|---|---|
| `running_value_rows.sql` | The rewrite: one value per order, then a running total per customer |
| `compare-output.txt` | What `compare_rows.py` printed against `running_value.sql` |
| `rows-output.txt` | The first ten rows |
| `time-output.txt` | The timings of both queries |

## What changed

Both this file and a correct rewrite add up each order once and then keep a running total with a window function
(`sum(...) OVER (...)`). They differ in two lines:

```diff
     sum(v.order_value) OVER (
         PARTITION BY v.customer_id
-        ORDER BY v.order_date
-        RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
+        ORDER BY v.order_date, v.order_id
+        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
     ) AS running_value
```

The part after `ORDER BY` is the window's frame: which rows count towards the total. `RANGE` counts every row up to
the current **date**, so two orders on the same date both get the day's full total, as the original query does with
`o2.order_date <= o.order_date`. `ROWS` counts up to the current **row**, so the first order of the day gets only
its own value. Leaving out the `RANGE` and `ROWS` line does not help either: with `order_id` in the `ORDER BY`, no
two rows tie, and the total grows row by row again.

## What the checks said

| Check | Result | Catches it? |
|---|---|---|
| Row count | 85,045, the same as the original | no |
| Speed | median 0.159 s against 0.454 s | no: a correct rewrite is just as fast |
| `compare_rows.py` | 25,911 rows differ in each direction, `DIFFERENT ROWS` | yes |
| The first rows | order 50492 on 2025-01-01: 690.00, where the original says 2575.26 | yes |

Customer 1 placed two orders on 1 January: 50492 worth 690.00 and 97958 worth 1,885.26. The original gives both
rows 2575.26, the day's total. This rewrite gives the first one 690.00. A report that reads the first order of a
day now shows the customer's value too low, on about three rows in ten.

## How you catch it

- **The row count** does not help: the same orders are there.
- **The timing** does not help: it only says the query is fast.
- **Comparing every value** does: `compare_rows.py` counts the rows each query returns that the other does not, and
  prints the first few.

To try it yourself, copy `running_value_rows.sql` into your `project` folder and ask Copilot to compare it with
`running_value.sql`.
