"""Release check: compare response times before and after a change.

Run it from this folder:

    python latency_check.py data/before.csv data/after.csv

It prints one line per endpoint and says whether the release can go ahead.
"""
import csv
import sys

LIMIT_PERCENT = 10


def read_times(path):
    """Return {endpoint: p95 time in milliseconds} from a CSV file."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["endpoint"]: int(row["p95_ms"]) for row in csv.DictReader(f)}


def change_percent(before_ms, after_ms):
    """How much slower the endpoint got, in percent. Negative means faster."""
    return (after_ms - before_ms) * 100 / before_ms


def is_too_slow(before_ms, after_ms):
    return change_percent(before_ms, after_ms) > LIMIT_PERCENT


def compare(before, after):
    """One row per endpoint in the after file: endpoint, before, after, change and status."""
    rows = []
    for endpoint, after_ms in after.items():
        before_ms = before.get(endpoint)
        if before_ms is None:
            rows.append((endpoint, None, after_ms, None, "new"))
        else:
            change = change_percent(before_ms, after_ms)
            status = "too slow" if is_too_slow(before_ms, after_ms) else "ok"
            rows.append((endpoint, before_ms, after_ms, change, status))
    return rows


def main(before_path, after_path):
    rows = compare(read_times(before_path), read_times(after_path))
    for endpoint, before_ms, after_ms, change, status in rows:
        before_text = "-" if before_ms is None else before_ms
        change_text = "" if change is None else f"{change:+.1f}%"
        print(f"{endpoint:<20} {before_text:>5} {after_ms:>5} {change_text:>7}  {status}")
    too_slow = [row[0] for row in rows if row[4] == "too slow"]
    if too_slow:
        print(f"Release blocked: {', '.join(too_slow)} too slow.")
        return 1
    print("Release can go ahead: no endpoint is too slow.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
