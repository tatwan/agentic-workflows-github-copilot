# Lab 03 resources

Two builds of the pipeline that turn green without fixing it. We wrote them for this lab so the result is the same
every time; they are not recorded Copilot runs. Use them when your own agent fixed the model properly, to see what
your two checks protect against.

| Folder | What changed | Build | Rows in `fct_orders` | Caught by |
|---|---|---|---:|---|
| [loosened-test](loosened-test/) | `models/schema.yml`: the two failing tests became warnings | `PASS=17 WARN=2 ERROR=0` | 35, of which 11 have a net amount | the list of changed files, and the rows |
| [dropped-rows](dropped-rows/) | `models/marts/fct_orders.sql`: `inner join` instead of `left join` | `PASS=19 WARN=0 ERROR=0` | 11 | the rows only |

Each folder holds the changed file, what `uv run dbt build` printed (`build-output.txt`) and what `dbt show`
printed afterwards (`rows-output.txt`). Both were run with dbt-core 1.12.5, dbt-duckdb 1.11.0 and DuckDB 1.5.6.

The project's data, `project/seeds/`, is synthetic: 40 orders and 14 discounts written for these labs under the
repository's [MIT licence](../../LICENSE). No real people, companies or orders.
