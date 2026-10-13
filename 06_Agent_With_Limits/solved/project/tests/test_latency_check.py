import unittest
from pathlib import Path

from latency_check import compare, is_too_slow, read_times

DATA = Path(__file__).resolve().parent.parent / "data"


class LatencyCheckTest(unittest.TestCase):
    def test_reads_the_before_file(self):
        times = read_times(DATA / "before.csv")
        self.assertEqual(len(times), 6)
        self.assertEqual(times["GET /orders"], 200)

    def test_five_percent_slower_is_ok(self):
        self.assertFalse(is_too_slow(120, 126))

    def test_exactly_ten_percent_is_ok(self):
        self.assertFalse(is_too_slow(200, 220))

    def test_fifteen_percent_slower_is_too_slow(self):
        self.assertTrue(is_too_slow(400, 460))

    def test_faster_is_ok(self):
        self.assertFalse(is_too_slow(150, 141))

    def test_new_endpoint_is_listed_as_new(self):
        rows = compare({}, {"GET /exports": 310})
        self.assertEqual(rows, [("GET /exports", None, 310, None, "new")])


if __name__ == "__main__":
    unittest.main()
