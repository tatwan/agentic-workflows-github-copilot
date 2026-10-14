from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from revenue import csv_text, write_csv


class MoneyDisplayTests(unittest.TestCase):
    def test_text_shows_two_places(self):
        for amount in (Decimal("1.0"), Decimal("1")):
            with self.subTest(amount=repr(amount)):
                self.assertEqual(csv_text([("2026-03", amount)]).splitlines()[1], "2026-03,1.00")

    def test_file_shows_two_places(self):
        for amount in (Decimal("1.0"), Decimal("1")):
            with self.subTest(amount=repr(amount)), TemporaryDirectory() as folder:
                path = Path(folder) / "monthly.csv"
                write_csv([("2026-03", amount)], path)
                self.assertEqual(path.read_text().splitlines()[1], "2026-03,1.00")
