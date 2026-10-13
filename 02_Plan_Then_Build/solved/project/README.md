# Orders report

A small Python report on the team's orders file. It reads `data/orders.csv` and summarises it by month: how many
orders, how many units and how much revenue.

One row of `data/orders.csv` is one **order line**: an order ID, a date, a region, a product, units and a unit
price. An order can have several lines, so the monthly order count counts distinct order IDs, not rows.

| File | What it holds |
|---|---|
| `orders/report.py` | `load_orders` reads the file; `monthly_summary` returns one row per month, oldest first. Revenue is a `Decimal`, so totals are exact |
| `tests/test_report.py` | Five tests for loading and the monthly summary |
| `data/orders.csv` | 97 order lines, January to June 2026. Synthetic data |

## Run the tests

From this folder:

```sh
python -m unittest
```

On Windows, use `py -m unittest` if `python` is not found. The project uses only the Python standard library
(Python 3.10 or newer); there is nothing to install.
