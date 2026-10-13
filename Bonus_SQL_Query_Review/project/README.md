# Orders SQL

The shop's orders in a [DuckDB](https://duckdb.org/) database, a database that lives in one file in this folder, so
there is no server to set up. The monthly customer report reads `running_value.sql`, and it has become slow.

| Path | What it holds |
|---|---|
| `schema.sql` | The three tables: `customers`, `orders` (status `complete`, `cancelled` or `pending`) and `line_items` (quantity and unit price per line) |
| `build_db.py` | Builds `orders.duckdb` from a fixed seed: 300 customers, 100,000 orders, 249,285 order lines. The same rows every time |
| `running_value.sql` | The report's query: one row per complete order, with the customer's running value |
| `run_query.py` | Runs a `.sql` file and prints the first rows; `--time` times it; `--explain` prints DuckDB's plan |
| `compare_rows.py` | Checks whether two queries return the same rows |
| `pyproject.toml`, `uv.lock` | The pinned version of DuckDB |

## Run it

From this folder:

```sh
uv run python build_db.py
uv run python run_query.py running_value.sql
uv run python run_query.py running_value.sql --time
uv run python compare_rows.py running_value.sql other_query.sql
```

The first time, uv downloads DuckDB and, if needed, a Python to run it; after that it starts at once. Every script
opens the database read-only, except `build_db.py`, which replaces it.

All data is synthetic.
