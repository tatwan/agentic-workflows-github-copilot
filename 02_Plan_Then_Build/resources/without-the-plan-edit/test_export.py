import csv
import tempfile
import unittest
from pathlib import Path

from orders.report import export_monthly_csv, load_orders


class ExportTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.output = Path(folder.name) / "monthly.csv"
        export_monthly_csv(load_orders(), self.output)
        with open(self.output, newline="", encoding="utf-8") as f:
            self.rows = list(csv.DictReader(f))

    def test_one_row_per_month(self):
        self.assertEqual([r["month"] for r in self.rows][:2], ["2026-01", "2026-02"])
        self.assertEqual(len(self.rows), 6)

    def test_january_matches_the_summary(self):
        january = self.rows[0]
        self.assertEqual(int(january["orders"]), 8)
        self.assertEqual(int(january["units"]), 174)
        self.assertEqual(float(january["revenue"]), 2085.70)


if __name__ == "__main__":
    unittest.main()
