"""Check that two queries return the same rows (Labs 03 and 05).

Run from the repository root, after  python sql/build_db.py :
    python sql/compare_rows.py sql/slow_orders.sql sql/slow_orders_rewrite.sql
Prints the row count of each query and of EXCEPT ALL in both directions. Both EXCEPT
counts must be 0. The database is opened read-only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

DB = Path(__file__).resolve().parent / "orders.duckdb"


def body(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip().rstrip(";")


def main(first: str, second: str) -> int:
    con = duckdb.connect(str(DB), read_only=True)
    a, b = body(first), body(second)
    n_a = con.execute(f"SELECT count(*) FROM ({a})").fetchone()[0]
    n_b = con.execute(f"SELECT count(*) FROM ({b})").fetchone()[0]
    a_not_b = con.execute(f"SELECT count(*) FROM (({a}) EXCEPT ALL ({b}))").fetchone()[0]
    b_not_a = con.execute(f"SELECT count(*) FROM (({b}) EXCEPT ALL ({a}))").fetchone()[0]
    print(f"rows in {first}: {n_a:,}")
    print(f"rows in {second}: {n_b:,}")
    print(f"in the first, not the second: {a_not_b:,}")
    print(f"in the second, not the first: {b_not_a:,}")
    same = n_a == n_b and a_not_b == 0 and b_not_a == 0
    print("SAME ROWS" if same else "DIFFERENT ROWS")
    return 0 if same else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python sql/compare_rows.py <first.sql> <second.sql>")
    if not DB.exists():
        sys.exit("sql/orders.duckdb not found: run  python sql/build_db.py  first")
    sys.exit(main(sys.argv[1], sys.argv[2]))
