from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from revenue import csv_text, write_csv


class NewValueTests(unittest.TestCase):
    def test_zero_and_negative(self):
        rows = [("2026-04", Decimal("0")), ("2026-05", Decimal("-2.5"))]
        original = rows.copy()
        expected = ["month,revenue", "2026-04,0.00", "2026-05,-2.50"]
        self.assertEqual(csv_text(rows).splitlines(), expected)
        with TemporaryDirectory() as folder:
            path = Path(folder) / "new.csv"
            write_csv(rows, path)
            self.assertEqual(path.read_text().splitlines(), expected)
        self.assertEqual(rows, original)

    def test_empty_file(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "empty.csv"
            write_csv([], path)
            self.assertEqual(path.read_text().splitlines(), ["month,revenue"])
