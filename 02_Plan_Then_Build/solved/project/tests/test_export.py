import contextlib
from datetime import date
from decimal import Decimal
import io
import tempfile
import unittest
from pathlib import Path

from orders.report import OrderLine, export_monthly_csv, load_orders, main


class ExportTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.output = Path(folder.name) / "monthly.csv"

    def read_lines(self):
        return self.output.read_text(encoding="utf-8").splitlines()

    def test_january_line_reads_as_finance_expects(self):
        export_monthly_csv(load_orders(), self.output)
        lines = self.read_lines()
        self.assertEqual(lines[0], "month,orders,units,revenue")
        self.assertEqual(lines[1], "2026-01,8,174,2085.70")
        self.assertEqual(len(lines), 7)

    def test_every_revenue_has_two_decimals(self):
        export_monthly_csv(load_orders(), self.output)
        for line in self.read_lines()[1:]:
            revenue = line.split(",")[3]
            self.assertRegex(revenue, r"^\d+\.\d\d$")

    def test_money_with_fewer_decimals_is_formatted(self):
        for price in ("1.0", "1"):
            with self.subTest(price=price):
                order = OrderLine(1, date(2026, 1, 1), "North", "Test", 1, Decimal(price))
                export_monthly_csv([order], self.output)
                self.assertEqual(self.read_lines()[1], "2026-01,1,1,1.00")

    def test_existing_file_is_replaced(self):
        self.output.write_text("old line\n" * 20, encoding="utf-8")
        export_monthly_csv(load_orders(), self.output)
        self.assertEqual(len(self.read_lines()), 7)

    def test_command_line_writes_the_file(self):
        with contextlib.redirect_stdout(io.StringIO()):
            main(["--output", str(self.output)])
        self.assertEqual(self.read_lines()[1], "2026-01,8,174,2085.70")


if __name__ == "__main__":
    unittest.main()
