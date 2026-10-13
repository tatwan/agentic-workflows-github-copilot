"""Run a .sql file against orders.duckdb and print the first rows.

Run from this folder, after  uv run python build_db.py :
    uv run python run_query.py running_value.sql
    uv run python run_query.py running_value.sql --time
    uv run python run_query.py running_value.sql --explain

--time runs the query once to warm up, then five more times, and prints each time and the median.
--explain prints DuckDB's plan with the time spent in each step (EXPLAIN ANALYZE).
The database is opened read-only, so no query can change the data.
"""
from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path

import duckdb

DB = Path(__file__).resolve().parent / "orders.duckdb"


def read_query(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip().rstrip(";")


def show(con: duckdb.DuckDBPyConnection, query: str, limit: int) -> None:
    cur = con.execute(query)
    names = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cells = [names] + [[str(v) for v in row] for row in rows[:limit]]
    widths = [max(len(r[i]) for r in cells) for i in range(len(names))]
    for n, r in enumerate(cells):
        print(" | ".join(v.rjust(w) for v, w in zip(r, widths)))
        if n == 0:
            print("-+-".join("-" * w for w in widths))
    print(f"({len(rows):,} rows)")


def timings(con: duckdb.DuckDBPyConnection, query: str, runs: int = 5) -> None:
    con.execute(query).fetchall()  # warm-up run, not counted
    seconds = []
    for _ in range(runs):
        start = time.perf_counter()
        con.execute(query).fetchall()
        seconds.append(time.perf_counter() - start)
    print("runs:   " + "  ".join(f"{s:.3f} s" for s in seconds))
    print(f"median: {statistics.median(seconds):.3f} s")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sql_file", type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--time", action="store_true", help="time five full runs")
    group.add_argument("--explain", action="store_true", help="print the plan with timings")
    parser.add_argument("--limit", type=int, default=10, help="rows to print (default 10)")
    args = parser.parse_args()

    if not DB.exists():
        sys.exit("orders.duckdb not found: run  uv run python build_db.py  first")
    query = read_query(args.sql_file)
    con = duckdb.connect(str(DB), read_only=True)
    if args.time:
        timings(con, query)
    elif args.explain:
        for _, plan in con.execute("EXPLAIN ANALYZE " + query).fetchall():
            print(plan)
    else:
        show(con, query, args.limit)
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
