# Bonus: How to speed up a SQL query without changing its answer

## Goal

Make a slow SQL query faster with Copilot and keep its answer exactly as it was. A rewrite can be faster and wrong:
the same number of rows in about a third of the time, with a different value on three rows in ten. So you decide
what the query returns before the agent starts, and you ask it to prove the rows match before it measures speed.

## What you will learn

- Read what a query returns, including what happens when two rows tie, before you ask for a rewrite.
- Ask for a rewrite in a new file, with what must stay the same and the order of the checks.
- Read a row comparison, and say why the same row count is not the same rows.
- Read a timing only after the rows match, and say what it can and cannot tell you.

## Before you start

You need VS Code with GitHub Copilot signed in, and uv ([Lab 00](../00_Setup_Check/), row 6, checks both). uv
downloads DuckDB and, if your computer has none, a Python the first time the project runs. You install nothing
else. You will read some SQL but not write any; Copilot writes and runs everything. [Lab 03](../03_Fix_A_Data_Pipeline/)
uses the same habit on a dbt pipeline; you do not need it first.

1. In VS Code choose **File > Open Folder** and open the `project` folder inside this lab
   (`Bonus_SQL_Query_Review/project`). Keep this README open somewhere else, for example on GitHub, so Copilot
   works on the query and not on the lab text.
2. If VS Code asks whether you trust the authors of the folder, choose to trust it.
3. Open the Chat view, start a **New Chat**, and choose **Interactive** (or **Agent**) in the mode picker, with
   Manual permissions.

The project is a shop's orders in [DuckDB](https://duckdb.org/), a database kept in one file in the folder.

| File | What it is |
|---|---|
| `build_db.py` | Builds `orders.duckdb` from a fixed seed: 300 customers, 100,000 orders. The same rows on every computer |
| `running_value.sql` | The slow query: one row per complete order, with the customer's running value |
| `run_query.py` | Runs a query and prints its first ten rows; `--time` runs it five times and prints the median |
| `compare_rows.py` | Checks whether two queries return the same rows, and prints the first rows that differ |

To start over at any point, hover over your first request in the chat and select **Restore Checkpoint**, or copy the
`project` folder again from the repository.

## Part A: Run the query and decide what right looks like

You work out what the query returns before anything changes, so you can judge whatever the agent writes.

1. Send this request:

   ```text
   Run uv run python build_db.py, then run running_value.sql with run_query.py
   and time it with --time. Tell me what the query computes. Don't change any files.
   ```

2. VS Code asks before each command runs. The first builds the database; the others only read it. Choose
   **Allow Once** each time. The first run downloads DuckDB, so give it a minute.
3. The build prints `orders: 100,000 rows`, and the query prints its first ten rows and `(85,045 rows)`, one per
   complete order. The first three:

   ```text
   customer_id | region | order_id | order_date | running_value
   ------------+--------+----------+------------+--------------
             1 |   West |    50492 | 2025-01-01 |       2575.26
             1 |   West |    97958 | 2025-01-01 |       2575.26
             1 |   West |    85296 | 2025-01-02 |       3350.96
   ```

4. Open `running_value.sql` and find the line `AND o2.order_date <= o.order_date`. For each order, the query adds up
   all of that customer's complete orders up to and including that **date**. So two orders on the same date get the
   same value: the day's total. Customer 1 placed two orders on 1 January, and both rows say 2575.26.
5. Note the median time: about 0.45 s on our machine; yours will differ. The query is slow because, for every
   order, it goes back over the customer's earlier orders again.
6. Write down what any rewrite must return: 85,045 rows, and 2575.26 on both of the first two rows.

Checkpoint: you have the row count, the two tied rows and their value, and the median time.

## Part B: Say what must stay the same, then ask for the rewrite

A request that only says "make it faster" leaves three choices to the agent: which file to change, what counts as the
same answer, and whether to check the rows at all. Your request makes all three.

1. In the same chat, send:

   ```text
   Write a faster version of running_value.sql as running_value_fast.sql. Keep the same
   columns, rows and order: two orders on the same date get the same running value.
   Don't change any other file. First prove the rows match with compare_rows.py,
   and time both queries with run_query.py --time only if they do.
   ```

2. Watch the steps: the agent reads the query and the tables in `schema.sql`, then creates `running_value_fast.sql`.
   Creating a file does not ask for approval; commands do.
3. Allow each command once. The comparison comes first and should end with `SAME ROWS`; then two timings.

Checkpoint: the agent compared the rows before it timed anything, and its summary says what the rewrite does
differently.

## Part C: Check the files, then the rows, then the speed

`SAME ROWS` is the agent's check. The next three are yours.

1. Select **View All File Changes** in the chat (or open each changed file from the list in the chat). The list
   should hold one new file, `running_value_fast.sql`. If `running_value.sql` is on it, the original changed, and
   a comparison against it proves nothing: restore the checkpoint and send the Part B request again.
2. Read the comparison the agent ran. It should say:

   ```text
   rows from running_value.sql: 85,045
   rows from running_value_fast.sql: 85,045
   in the first, not the second: 0
   in the second, not the first: 0
   same order: yes
   SAME ROWS
   ```

   The two `in the ...` lines compare every value of every row, not only how many rows there are.
3. Now the tie you wrote down. Send:

   ```text
   Show me the first ten rows of running_value_fast.sql.
   ```

   Rows 1 and 2 are orders 50492 and 97958, both 2575.26, and row 3 is 3350.96. Open `running_value_fast.sql`.
   A rewrite usually adds up each order once and then keeps a running total with `sum(...) OVER (...)`. If yours
   does, the `ORDER BY` inside `OVER (...)` should sort by the date alone, followed by a `RANGE` line or nothing.
   Part D shows what goes wrong with `ROWS`.
4. Last, the speed. On our machine the median went from about 0.45 s to about 0.16 s, nearly three times faster.
   Your times will differ: compare the two queries on your own machine, in the same run.

Checkpoint: one new file, `SAME ROWS`, the tied rows match what you wrote in Part A, and a median time for each
query.

## Part D: Catch a rewrite that is fast and wrong

A timing never tells you whether the answer held. We wrote a rewrite that is fast and wrong, in
[resources/rows-frame](resources/rows-frame/), with what each check printed for it. It is not a recorded Copilot run.

1. Open [resources/rows-frame](resources/rows-frame/). The query looks like a good rewrite. Its window sorts by date
   and order ID with `ROWS`, so the running total grows one row at a time, and the first order of a day gets only
   its own value.
2. To see it on your machine, copy `running_value_rows.sql` into your `project` folder and send:

   ```text
   Compare running_value.sql with running_value_rows.sql using compare_rows.py,
   then show me the first ten rows of running_value_rows.sql.
   ```

   The comparison says `DIFFERENT ROWS`: 25,911 rows in each direction. The first row says 690.00, order 50492
   alone, where the original says 2575.26.
3. Compare the three:

   | Query | Rows | `compare_rows.py` | Order 50492 | Median time |
   |---|---:|---|---:|---:|
   | `running_value.sql` | 85,045 | | 2575.26 | about 0.45 s |
   | Your rewrite | 85,045 | `SAME ROWS` | 2575.26 | about 0.16 s |
   | `running_value_rows.sql` | 85,045 | `DIFFERENT ROWS` | 690.00 | about 0.16 s |

Checkpoint: you can say which checks catch the wrong rewrite. The row count and the timing do not: it has every row
and is as fast as yours. The comparison and the tied rows do.

## If your run looks different

| What you see | What to do |
|---|---|
| `uv` is not found | Do row 6 of [Lab 00](../00_Setup_Check/), then close and reopen VS Code |
| The first run cannot download packages | Your network may block the Python package index. Ask your IT team for the approved proxy or mirror |
| The agent asks to run `pip install duckdb` | Skip it: `uv run` installs what the project needs |
| `orders.duckdb not found: run  uv run python build_db.py  first` | The database is not built yet. Ask the agent to run `build_db.py` |
| `IO Error: Could not set lock on file ".../orders.duckdb"` | Another program has the database open, such as a database extension or a second chat's command. Close it and run the command again |
| The agent changed `running_value.sql` | Restore the checkpoint and send the Part B request again, adding `Don't change running_value.sql.` |
| The agent timed the queries without comparing the rows | Ask: `Run compare_rows.py on the two files and show me what it prints.` |
| `DIFFERENT ROWS` | Tell the agent: `Two orders on the same date must get the same running value. Fix running_value_fast.sql and compare again.` |

## What you can do now

- Read what a query returns, and find the rows where a tie decides the answer.
- Write a request that names the new file, what must stay the same, and which check comes first.
- Read a row comparison, and explain why 85,045 rows on both sides did not mean the same rows.
- Read a timing after the rows match, and say why a fast query can still be the wrong one.

## Challenge

1. **The request without the rules.** Copy a fresh `project` folder, open it, start a New Chat and send
   `running_value.sql is slow. Make it faster.` Then do Part C: which file changed, did the agent compare the rows,
   and what do the first two rows say? Expected: it varies from run to run. If the agent rewrote `running_value.sql`
   in place, copy the original from the repository in as `running_value_original.sql` and ask for the comparison.
2. **Test the tie on a tiny case.** Send:

   ```text
   Test both queries on a tiny database in memory, without touching orders.duckdb:
   one customer, two complete orders on the same day worth 10.00 and 20.00,
   one the next day worth 5.00, and a cancelled order. Show me the running values.
   ```

   Check the numbers by hand: 10 + 20 = 30 for both orders of the first day, then 35, and the cancelled order counts
   for nothing. Expected: `30.00 / 30.00 / 35.00` from both queries. If you copied `running_value_rows.sql` in
   Part D, ask for it too: `10.00 / 30.00 / 35.00`.

Answers to compare with when you finish, for the lab and the challenge: [`solved/`](solved/).

## Going further

- **Read the plan.** `uv run python run_query.py running_value.sql --explain` prints DuckDB's plan with the time
  each step took. Ask Copilot to run it on both queries and tell you which step took the most time in each.
- **Make the rule permanent.** Add a line such as `Before you time a rewritten query, prove it returns the same
  rows with compare_rows.py.` to `.github/copilot-instructions.md`, as in [Lab 04](../04_Team_Rules/).
- **One machine is one answer.** A timing holds for this data on this computer. More data, other hardware or many
  users at once can change it, so measure where the query really runs.

## Resources

- [DuckDB window functions](https://duckdb.org/docs/current/sql/functions/window_functions.html), and its
  [framing section](https://duckdb.org/docs/current/sql/functions/window_functions.html#framing) on `ROWS` and `RANGE`
- [Set operations: EXCEPT ALL](https://duckdb.org/docs/current/sql/query_syntax/setops.html)
- [EXPLAIN ANALYZE: profile queries](https://duckdb.org/docs/current/guides/meta/explain_analyze.html)
- [Review the agent's edits and use checkpoints](https://code.visualstudio.com/docs/agents/run/review-code-edits)
- [Approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals)
- [Working on projects with uv](https://docs.astral.sh/uv/guides/projects/)
