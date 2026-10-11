"""Run Lab 00's four baselines from any directory.

From orders-analytics/: uv run python ../00_Environment_Check/resources/check_setup.py
Use --project PATH to check a separate project copy, and --verbose for full output.
Exit status is 1 if any baseline fails; subsequent checks still run.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_ROWS = {"customers": 300, "orders": 100000, "line_items": 249285, "slow_orders.sql rows": 85045}


def command(args: list[str], cwd: Path) -> tuple[int, str]:
    try:
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=300)
        return result.returncode, result.stdout + result.stderr
    except (OSError, subprocess.TimeoutExpired) as error:
        return 1, str(error)


def pytest_check(project: Path) -> tuple[bool, str, str]:
    code, output = command([sys.executable, "-m", "pytest", "-q"], project / "python")
    passed = re.search(r"(\d+) passed", output)
    ok = code == 0 and passed is not None and int(passed[1]) == 5
    return ok, "5 passed" if ok else "expected 5 passing tests; see output", output


def maven_check(project: Path) -> tuple[bool, str, str]:
    wrapper = project / "java" / ("mvnw.cmd" if os.name == "nt" else "mvnw")
    code, output = command([str(wrapper), "test"], project / "java")
    totals = re.findall(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)\s*$", output, re.M)
    ok = code == 0 and bool(totals) and totals[-1] == ("5", "0", "0", "0")
    return ok, "5 tests, 0 failures, 0 errors, 0 skipped" if ok else "expected 5 passing tests; see output", output


def sql_check(project: Path) -> tuple[bool, str, str]:
    code, output = command([sys.executable, "sql/build_db.py"], project)
    if code != 0:
        return False, "database build failed; see output", output
    import duckdb

    with duckdb.connect(str(project / "sql/orders.duckdb"), read_only=True) as connection:
        rows = dict(connection.execute((project / "sql/row_count.sql").read_text()).fetchall())
    summary = ", ".join(f"{name} {count:,}" for name, count in rows.items())
    return rows == EXPECTED_ROWS, summary, output


def dbt_check(project: Path) -> tuple[bool, str, str]:
    dbt = Path(sys.executable).parent / ("dbt.exe" if os.name == "nt" else "dbt")
    code, output = command([str(dbt), "build", "--profiles-dir", "."], project / "dbt")
    counts = dict(re.findall(r"(PASS|WARN|ERROR|SKIP|TOTAL)=(\d+)", output))
    ok = code == 0 and counts == {"PASS": "17", "WARN": "0", "ERROR": "0", "SKIP": "0", "TOTAL": "17"}
    return ok, "PASS=17 WARN=0 ERROR=0 SKIP=0 TOTAL=17" if ok else "expected PASS=17; see output", output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[2] / "orders-analytics")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    project = args.project.resolve()
    print(f"Python {sys.version.split()[0]}")
    failures = 0
    for name, check in [("pytest", pytest_check), ("Maven Wrapper", maven_check), ("SQL row counts", sql_check), ("dbt build", dbt_check)]:
        try:
            ok, summary, output = check(project)
        except (ImportError, OSError, RuntimeError) as error:
            ok, summary, output = False, "check could not finish", str(error)
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {summary}")
        if args.verbose or not ok:
            print(output.strip())
        failures += not ok
    print(f"{4 - failures}/4 baselines passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
