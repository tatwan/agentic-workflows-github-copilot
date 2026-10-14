"""Export already-calculated monthly revenue. Uses only the standard library."""
import csv
from io import StringIO
from pathlib import Path


def csv_text(rows):
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["month", "revenue"])
    for month, revenue in rows:
        writer.writerow([month, str(revenue)])
    return output.getvalue()


def write_csv(rows, path):
    with Path(path).open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["month", "revenue"])
        for month, revenue in rows:
            writer.writerow([month, str(revenue)])
