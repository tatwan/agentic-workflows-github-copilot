# Lab 03: How to fix a data pipeline without weakening its tests

## Goal

Fix a failing dbt pipeline with Copilot and keep its tests as strict as they were. When a build fails, the quickest
way to green is to loosen the test that failed, or to drop the rows it fails on. Both make the build pass and leave
the data wrong. So before the agent starts, you say which files may change, and after it finishes, you check the
rows against numbers you worked out yourself.

## What you will learn

- Read a failing dbt build and trace each failing test to the rows behind it.
- Tell the agent which files may change and which must stay as they are.
- Review the list of changed files for edits to tests, not only to the model.
- Check a table's rows against numbers you took from the source data.

## Before you start

You need VS Code with GitHub Copilot signed in, and uv ([Lab 00](../00_Setup_Check/), row 6, checks both). uv
downloads dbt, DuckDB and, if your computer has none, a Python the first time the project runs. You install
nothing else. You will read some SQL and YAML but not write any; Copilot edits and runs everything.

1. In VS Code choose **File > Open Folder** and open the `project` folder inside this lab
   (`03_Fix_A_Data_Pipeline/project`). Keep this README open somewhere else, for example on GitHub, so Copilot
   works on the pipeline and not on the lab text.
2. If VS Code asks whether you trust the authors of the folder, choose to trust it.
3. Open the Chat view, start a **New Chat**, and choose **Interactive** (or **Agent**) in the mode picker, with
   Manual permissions.

The project is a small [dbt](https://docs.getdbt.com/) pipeline on DuckDB, a database kept in one file in the
folder.

| File | What it is |
|---|---|
| `seeds/raw_orders.csv` | 40 orders: ID, customer, date, status (`complete` or `cancelled`), gross amount |
| `seeds/raw_discounts.csv` | 14 discounts. An order without a discount has no row here |
| `models/staging/` | Two models that give the raw rows their types |
| `models/marts/fct_orders.sql` | The table finance reads: one row per complete order, with its discount and net amount |
| `models/schema.yml` | The tests. Team rule: every column of `fct_orders` has a `not_null` test |

Three dbt words you need. A **seed** is a CSV file dbt loads as a table. A **model** is a `select` saved in a
`.sql` file; dbt builds a view or a table from it. A **test** is a query that looks for bad rows: it passes when it
finds none. `dbt build` loads the seeds, builds the models and runs the tests.

To start over at any point, hover over your first request in the chat and select **Restore Checkpoint**, or copy the
`project` folder again from the repository.

## Part A: Run the build and decide what right looks like

You work out the correct rows before the agent touches anything, so you can judge whatever it does.

1. Send this request:

   ```text
   Run uv run dbt build and tell me which tests fail and why.
   Don't change any files.
   ```

2. VS Code asks before the command runs. Read it: it builds the tables and runs the tests, and changes no file you
   wrote. Choose **Allow Once**. The first run downloads dbt and DuckDB, so give it a minute.
3. The build ends with this line:

   ```text
   Done. PASS=17 WARN=0 ERROR=2 SKIP=0 NO-OP=0 REUSED=0 TOTAL=19
   ```

   The two failing tests are `not_null_fct_orders_discount_amount` and `not_null_fct_orders_net_amount`, and each
   says `Got 24 results`: 24 rows with an empty value. The agent should explain why. The model joins orders to
   discounts with a `left join`, which keeps an order that has no discount and leaves its discount empty (`NULL`).
   Gross minus an empty value is empty too, so `net_amount` is empty on the same 24 rows.
4. Check the source yourself. Open `seeds/raw_orders.csv`, press Ctrl+F (Cmd+F on a Mac) and search for
   `,complete,`. The search box shows 35 matches: `fct_orders` should have 35 rows.
5. Look at two orders. Order 1 is complete, gross 267.36, and `raw_discounts.csv` has no row for it. Order 4 is
   complete, gross 46.55, with a 10.00 discount. Write down what `fct_orders` should hold:

   | order_id | gross_amount | discount_amount | net_amount |
   |---:|---:|---:|---:|
   | 1 | 267.36 | 0 | 267.36 |
   | 4 | 46.55 | 10.00 | 36.55 |

Checkpoint: the build failed two tests on 24 rows each, and you have written 35 rows, order 1 and order 4.

## Part B: Say what may change, then ask for the fix

There are three ways to make these two tests pass:

- **Fix the model**, so an order without a discount gets a discount of 0.
- **Loosen the tests**, for example delete them or turn them into warnings.
- **Drop the rows** they fail on, for example with an `inner join`, which keeps only orders that have a discount.

Only the first gives finance the right numbers. A request that only says "make the build pass" leaves the choice to
the agent. Your request makes it.

1. In the same chat, send:

   ```text
   Fix fct_orders so the build passes. An order with no discount has a discount of 0.
   Only change models/marts/fct_orders.sql. Keep the tests and the seeds as they are,
   and keep every complete order in the table. Run the build when you are done.
   ```

2. Watch the steps: the agent reads the model and the tests, then edits `fct_orders.sql`. Edits do not ask for
   approval; commands do.
3. When it asks to run `uv run dbt build`, choose **Allow Once**. The build now ends:

   ```text
   Done. PASS=19 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=19
   ```

Checkpoint: the build passes 19 of 19, and the agent's summary says what it changed in `fct_orders.sql`.

## Part C: Check the files, then check the rows

Green is the agent's check. The next two are yours, one for each half of your request.

1. Select **View All File Changes** in the chat (or open each changed file from the list in the chat). The list
   should hold one file: `models/marts/fct_orders.sql`. If `schema.yml` or a seed is on it, a test or the data was
   changed: restore the checkpoint and send the Part B request again.
2. In the diff of `fct_orders.sql`, check three things:
   - An empty discount becomes 0 in both columns, for example `coalesce(d.discount_amount, 0)` in
     `discount_amount` and in the subtraction for `net_amount`.
   - The join is still a `left join`.
   - `where o.status = 'complete'` is still there.
3. Now the rows. Send:

   ```text
   Use dbt show to tell me how many rows fct_orders has, how many have a net_amount,
   and the rows for orders 1 and 4.
   ```

4. Allow each `dbt show` command once. `dbt show` runs a query and prints the result as a table. Your numbers
   should be:

   ```text
   | orders | with_net |
   | ------ | -------- |
   |     35 |       35 |

   | order_id | customer_id | order_date | gross_amount | discount_amount | net_amount |
   | -------- | ----------- | ---------- | ------------ | --------------- | ---------- |
   |        1 |         103 | 2026-03-21 |       267.36 |               0 |     267.36 |
   |        4 |         107 | 2026-03-06 |        46.55 |              10 |      36.55 |
   ```

   `dbt show` prints `10` for 10.00. The agent's queries may differ from ours: compare the numbers, not the
   layout.

Checkpoint: one changed file, 35 rows with 35 net amounts, and orders 1 and 4 match what you wrote in Part A.

## Part D: Two quick ways to green

Whatever your agent did, the build alone does not tell you which way it went green. We wrote two builds for this
lab that turn green the other ways, in the [resources](resources/) folder with what dbt printed for each. They are
not recorded Copilot runs.

1. Open [resources/loosened-test](resources/loosened-test/). The model is unchanged; `schema.yml` sets the two
   failing tests to `severity: warn`. A warning does not stop a build, so it succeeds.
2. Open [resources/dropped-rows](resources/dropped-rows/). Only `fct_orders.sql` changed: `inner join` instead of
   `left join`. The build prints the same line as your fix. `not_null` checks the rows that are in the table, not
   the ones that are missing.
3. Compare the three:

   | Build | Files changed | Build result | Rows | Order 1 net | Net sales |
   |---|---|---|---:|---:|---:|
   | Your fix | `fct_orders.sql` | PASS=19 | 35 | 267.36 | 6,417.95 |
   | Loosened tests | `schema.yml` | PASS=17 WARN=2 | 35 | empty | 2,120.10 |
   | Dropped rows | `fct_orders.sql` | PASS=19 | 11 | missing | 2,120.10 |

Checkpoint: you can say which of your checks catches each one. The changed files catch the loosened tests. Only the
rows catch the dropped rows, because that build kept to the rule on files.

## If your run looks different

| What you see | What to do |
|---|---|
| `uv` is not found | Do row 6 of [Lab 00](../00_Setup_Check/), then close and reopen VS Code |
| The first build cannot download packages | Your network may block the Python package index. Ask your IT team for the approved proxy or mirror |
| The agent asks to run `pip install dbt-duckdb` or `uv sync` | Skip `pip install`: `uv run` installs what the project needs. `uv sync` is fine to allow |
| `IO Error: Could not set lock on file ".../orders.duckdb"` | Another program has the database open, such as a database extension or a second chat's command. Close it and run the build again |
| The agent changed `schema.yml` or a seed | Restore the checkpoint and send the Part B request again, adding `Don't change models/schema.yml.` |
| PASS=19 but fewer than 35 rows | The agent dropped rows. Tell it: `Order 1 is missing. Keep every complete order and give a missing discount 0.` |

## What you can do now

- Read a failing dbt build and trace a test's failing rows back to the source files.
- Write a request that says which files may change and what must stay true of the data.
- Check the changed files for edits to tests or source data.
- Check a row count and two known rows against the source, and explain why a passing build with 11 rows is wrong.

## Challenge

1. **The request without the rules.** Copy a fresh `project` folder, open it, start a New Chat and send
   `The dbt build fails. Make it pass.` Then do Part C: which files changed, and how many rows does `fct_orders`
   have? Expected: it varies from run to run, and you find out from the changed files and the rows, not from the
   green build.
2. **Turn the row check into a test.** In your fixed project, send:

   ```text
   Add a dbt test in tests/ that fails if a complete order in stg_orders is missing
   from fct_orders. Don't change any other file. Run the build.
   ```

   Expected: `PASS=20 ... TOTAL=20`. To see the test catch dropped rows, ask:
   `Change the left join in fct_orders to an inner join and run the build. Then change it back and build again.`
   The first build fails the new test with `Got 24 results` (`PASS=19 ... ERROR=1`); the second passes 20 of 20.
   Check that `fct_orders.sql` ends with a `left join` again.

Answers to compare with when you finish, for the lab and the challenge: [`solved/`](solved/).

## Going further

- **Unit tests.** A dbt unit test gives a model a few hand-written input rows (an order with a discount, one
  without) and the rows you expect back, and checks the SQL logic before the table is built. Ask Copilot to add one
  for orders 1 and 4.
- **Make the rule permanent.** Add a line such as `Never loosen or delete a test to make a build pass; ask me
  first.` to `.github/copilot-instructions.md`, as in [Lab 04](../04_Team_Rules/).
- **Connect Copilot to dbt itself.** In this lab the agent runs dbt through the terminal and reads the files. An MCP
  server gives it dbt as tools instead: the [dbt MCP server](https://github.com/dbt-labs/dbt-mcp) offers `build`,
  `test`, `show` and lineage of a model, and works with dbt Core projects like this one. It is configured in
  `.mcp.json` (or `.vscode/mcp.json`), and with Manual permissions VS Code can ask before each tool call. Its dbt
  commands can change your models and warehouse objects, so read each call before you allow it, and check whether
  your organisation allows MCP servers first. The same idea connects Copilot to Databricks, a database or a ticket
  system.
- **Speed up a query without changing its answer.** The [SQL bonus](../Bonus_SQL_Query_Review/) uses the same
  habit on a slow SQL query: say what must stay the same, prove the rows match, and only then time it.

## Resources

- [dbt build](https://docs.getdbt.com/reference/commands/build) and [data tests](https://docs.getdbt.com/docs/build/data-tests)
- [Test severity: warn and error](https://docs.getdbt.com/reference/resource-configs/severity)
- [dbt show](https://docs.getdbt.com/reference/commands/show) and [unit tests](https://docs.getdbt.com/docs/build/unit-tests)
- [Review the agent's edits and use checkpoints](https://code.visualstudio.com/docs/agents/run/review-code-edits)
- [Approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals)
- [Working on projects with uv](https://docs.astral.sh/uv/guides/projects/)
- [Add and manage MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
