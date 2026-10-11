"""Run a .sql file against sql/orders.duckdb and print the rows.

Run from the repository root:  python sql/run_query.py sql/row_count.sql
Add --explain to print the plan with timings (EXPLAIN ANALYZE). Use --explain on
SELECT statements only: EXPLAIN ANALYZE runs the statement.
The database is opened read-only, so no statement can change data.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

DB = Path(__file__).resolve().parent / "orders.duckdb"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sql_file", type=Path)
    parser.add_argument("--explain", action="store_true", help="print EXPLAIN ANALYZE output")
    parser.add_argument("--limit", type=int, default=10, help="rows to print (default 10)")
    args = parser.parse_args()

    if not DB.exists():
        raise SystemExit("sql/orders.duckdb not found: run  python sql/build_db.py  first")
    query = args.sql_file.read_text(encoding="utf-8").strip().rstrip(";")
    con = duckdb.connect(str(DB), read_only=True)
    if args.explain:
        for _, plan in con.execute("EXPLAIN ANALYZE " + query).fetchall():
            print(plan)
        return
    cur = con.execute(query)
    names = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print(" | ".join(names))
    for row in rows[: args.limit]:
        print(" | ".join(str(v) for v in row))
    print(f"({len(rows):,} rows)")


if __name__ == "__main__":
    main()
