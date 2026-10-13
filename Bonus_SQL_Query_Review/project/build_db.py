"""Build orders.duckdb: synthetic orders made from a fixed seed.

Run from this folder:  uv run python build_db.py
Running it again replaces the file and gives the same rows every time.
"""
from __future__ import annotations

import csv
import random
import tempfile
from datetime import date, timedelta
from pathlib import Path

import duckdb

SEED = 20261006
N_CUSTOMERS = 300
N_ORDERS = 100_000
N_PRODUCTS = 120
REGIONS = ["North", "South", "East", "West"]
SEGMENTS = ["retail", "wholesale", "online"]
STATUSES = ["complete"] * 17 + ["cancelled"] * 2 + ["pending"]

HERE = Path(__file__).resolve().parent
DB = HERE / "orders.duckdb"


def make_rows() -> dict[str, list[tuple]]:
    rng = random.Random(SEED)
    customers = [
        (cid, f"Customer {cid:04d}", rng.choice(REGIONS), rng.choice(SEGMENTS))
        for cid in range(1, N_CUSTOMERS + 1)
    ]
    prices = {pid: round(rng.uniform(2, 80), 2) for pid in range(1, N_PRODUCTS + 1)}
    start = date(2025, 1, 1)
    orders, line_items = [], []
    for oid in range(1, N_ORDERS + 1):
        cid = rng.randint(1, N_CUSTOMERS)
        day = start + timedelta(days=rng.randint(0, 364))
        orders.append((oid, cid, day.isoformat(), rng.choice(STATUSES)))
        for line_no in range(1, rng.randint(1, 4) + 1):
            pid = rng.randint(1, N_PRODUCTS)
            line_items.append((oid, line_no, pid, rng.randint(1, 12), f"{prices[pid]:.2f}"))
    return {"customers": customers, "orders": orders, "line_items": line_items}


def build(db_path: Path = DB) -> dict[str, int]:
    if db_path.exists():
        db_path.unlink()
    con = duckdb.connect(str(db_path))
    con.execute((HERE / "schema.sql").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as folder:
        for table, rows in make_rows().items():
            path = Path(folder) / f"{table}.csv"
            with path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
            con.execute(f"COPY {table} FROM '{path.as_posix()}' (HEADER false)")
    counts = {
        table: con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        for table in ("customers", "orders", "line_items")
    }
    con.close()
    return counts


if __name__ == "__main__":
    for table, n in build().items():
        print(f"{table}: {n:,} rows")
    print(f"written: {DB.name}")
