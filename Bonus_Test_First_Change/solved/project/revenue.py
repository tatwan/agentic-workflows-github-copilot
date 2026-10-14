"""Export already-calculated monthly revenue. Uses only the standard library."""
import csv
from io import StringIO
from pathlib import Path


def _write_rows(rows, output):
    writer = csv.writer(output)
    writer.writerow(["month", "revenue"])
    for month, revenue in rows:
        writer.writerow([month, f"{revenue:.2f}"])


def csv_text(rows):
    output = StringIO(newline="")
    _write_rows(rows, output)
    return output.getvalue()


def write_csv(rows, path):
    with Path(path).open("w", newline="", encoding="utf-8") as output:
        _write_rows(rows, output)
