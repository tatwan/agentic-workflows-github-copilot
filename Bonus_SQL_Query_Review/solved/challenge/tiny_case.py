"""Challenge 2 (one possible answer): run each query on a four-order database in memory.

Run from the project folder:  uv run python tiny_case.py running_value.sql running_value_fast.sql
"""
import sys
from pathlib import Path

import duckdb

con = duckdb.connect(":memory:")
con.execute(Path("schema.sql").read_text(encoding="utf-8"))
con.execute("INSERT INTO customers VALUES (1, 'Customer 0001', 'North', 'retail')")
con.execute("""INSERT INTO orders VALUES
    (1, 1, '2025-01-01', 'complete'),
    (2, 1, '2025-01-01', 'complete'),
    (3, 1, '2025-01-02', 'complete'),
    (4, 1, '2025-01-01', 'cancelled')""")
con.execute("""INSERT INTO line_items VALUES
    (1, 1, 1, 1, 10.00),
    (2, 1, 1, 2, 10.00),
    (3, 1, 1, 1, 5.00),
    (4, 1, 1, 1, 999.00)""")
for name in sys.argv[1:]:
    query = Path(name).read_text(encoding="utf-8").strip().rstrip(";")
    values = [str(row[-1]) for row in con.execute(query).fetchall()]
    print(f"{name}: {' / '.join(values)}")
