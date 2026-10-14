from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from revenue import csv_text, write_csv


class ExistingExportTests(unittest.TestCase):
    def test_header(self):
        self.assertEqual(csv_text([]), "month,revenue\r\n")

    def test_two_decimal_values_and_order(self):
        rows = [("2026-01", Decimal("12.50")), ("2026-02", Decimal("8.25"))]
        self.assertEqual(csv_text(rows).splitlines(),
                         ["month,revenue", "2026-01,12.50", "2026-02,8.25"])

    def test_file_matches_text(self):
        rows = [("2026-01", Decimal("12.50"))]
        with TemporaryDirectory() as folder:
            path = Path(folder) / "monthly.csv"
            write_csv(rows, path)
            with path.open(newline="", encoding="utf-8") as output:
                self.assertEqual(output.read(), csv_text(rows))

    def test_input_unchanged(self):
        rows = [("2026-01", Decimal("12.50"))]
        original = rows.copy()
        csv_text(rows)
        self.assertEqual(rows, original)
