# Orders pipeline

A small [dbt](https://docs.getdbt.com/) project that turns the shop's raw order files into `fct_orders`, the table
finance reads for net sales. It runs on [DuckDB](https://duckdb.org/), a database that lives in one file in this
folder, so there is no server to set up.

| Path | What it holds |
|---|---|
| `seeds/raw_orders.csv` | 40 orders: order ID, customer, date, status (`complete` or `cancelled`), gross amount |
| `seeds/raw_discounts.csv` | 14 discounts, one row per discounted order. An order without a discount has no row |
| `models/staging/` | `stg_orders` and `stg_discounts`: the raw rows with their types (dates, money with two decimals) |
| `models/marts/fct_orders.sql` | One row per complete order, with its discount and net amount |
| `models/schema.yml` | The tests. Team rule: every column of `fct_orders` has a `not_null` test |
| `pyproject.toml`, `uv.lock` | The pinned versions of dbt and DuckDB |
| `dbt_project.yml`, `profiles.yml` | dbt's settings and where the DuckDB file goes (`orders.duckdb`) |

## Run it

From this folder:

```sh
uv run dbt build
```

`dbt build` loads the seeds, builds the models and runs every test, in order. The first time, uv downloads dbt,
DuckDB and, if needed, a Python to run them; after that it starts at once.

To look at rows, use `dbt show`, for example:

```sh
uv run dbt show --select fct_orders
uv run dbt show --inline "select count(*) from {{ ref('fct_orders') }}"
```

All data is synthetic.
