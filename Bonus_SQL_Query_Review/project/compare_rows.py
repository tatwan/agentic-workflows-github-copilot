"""Check that two queries return the same rows.

Run from this folder, after  uv run python build_db.py :
    uv run python compare_rows.py running_value.sql running_value_fast.sql

Prints how many rows each query returns, how many rows are in one and not the other
(counting repeated rows, with EXCEPT ALL), whether the rows come back in the same order,
and the first few rows that differ. The database is opened read-only.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import duckdb

DB = Path(__file__).resolve().parent / "orders.duckdb"


def read_query(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip().rstrip(";")


def first_extra(rows: list[tuple], extra: list[tuple], n: int = 3) -> list[tuple]:
    """The first n rows, in the query's own order, that the other query does not return."""
    left, found = Counter(extra), []
    for row in rows:
        if left[row] > 0:
            left[row] -= 1
            found.append(row)
            if len(found) == n:
                break
    return found


def main(first: str, second: str) -> int:
    con = duckdb.connect(str(DB), read_only=True)
    a, b = read_query(first), read_query(second)
    rows_a = con.execute(a).fetchall()
    rows_b = con.execute(b).fetchall()
    only_a = con.execute(f"({a}) EXCEPT ALL ({b})").fetchall()
    only_b = con.execute(f"({b}) EXCEPT ALL ({a})").fetchall()
    con.close()

    print(f"rows from {first}: {len(rows_a):,}")
    print(f"rows from {second}: {len(rows_b):,}")
    print(f"in the first, not the second: {len(only_a):,}")
    print(f"in the second, not the first: {len(only_b):,}")
    same_rows = len(rows_a) == len(rows_b) and not only_a and not only_b
    if same_rows:
        print("same order: " + ("yes" if rows_a == rows_b else "no"))
    else:
        for label, rows, extra in ((first, rows_a, only_a), (second, rows_b, only_b)):
            if extra:
                print(f"first rows only in {label}:")
                for row in first_extra(rows, extra):
                    print("  " + " | ".join(str(v) for v in row))
    print("SAME ROWS" if same_rows else "DIFFERENT ROWS")
    return 0 if same_rows else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: uv run python compare_rows.py <first.sql> <second.sql>")
    if not DB.exists():
        sys.exit("orders.duckdb not found: run  uv run python build_db.py  first")
    sys.exit(main(sys.argv[1], sys.argv[2]))
