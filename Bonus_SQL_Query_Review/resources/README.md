# Bonus resources

A rewrite of the report's query that is fast and wrong. We wrote it for this lab so the result is the same every
time; it is not a recorded Copilot run. Use it when your own agent's rewrite returned the same rows, to see what
the row check protects against.

| Folder | What changed | Rows | `compare_rows.py` | Median time |
|---|---|---:|---|---:|
| [rows-frame](rows-frame/) | The running total adds orders one row at a time, so two orders on the same date get different values | 85,045 | `DIFFERENT ROWS`: 25,911 rows differ | 0.159 s, against 0.454 s for the original |

The folder holds the query, what `compare_rows.py` printed (`compare-output.txt`), the first rows
(`rows-output.txt`) and the timings (`time-output.txt`). They were run with DuckDB 1.5.6 on a four-core Linux
machine; your times will differ, so compare the two queries on your own machine.

The data in `project/` is synthetic: `build_db.py` makes it from a fixed seed, under the repository's
[MIT licence](../../LICENSE). No real people, companies or orders.
