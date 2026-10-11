"""Independent acceptance: frozen source, literal expected rows, integer cents."""
import argparse
import csv
import hashlib
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('report', type=Path)
parser.add_argument('--case', choices=['core', 'challenge'], default='core')
args = parser.parse_args()
resources = Path(__file__).parent
fixture = resources / ('orders.csv' if args.case == 'core' else 'challenge.csv')

def fail(message):
    parser.exit(1, f'FAIL {message}\n')

if not args.source.is_file():
    fail('source CSV not found')
if hashlib.sha256(args.source.read_bytes()).digest() != hashlib.sha256(fixture.read_bytes()).digest():
    fail('source differs from the supplied fixture')
if not args.report.is_file():
    fail('report CSV not found')

# Written from hand calculations before either model or summary script runs.
expected = [('East', '3', '2', '33', '320.50'), ('South', '2', '1', '28', '405.50'), ('West', '3', '1', '29', '202.25')]
if args.case == 'challenge':
    expected = [('East', '3', '2', '34', '324.00'), ('North', '1', '1', '12', '42.00'), ('South', '2', '1', '28', '405.50'), ('West', '3', '1', '29', '202.25')]
with args.report.open(newline='') as report:
    reader = csv.reader(report)
    if next(reader, None) != ['region', 'lines', 'orders', 'units', 'revenue']:
        fail('header must be region,lines,orders,units,revenue')
    actual = list(reader)
if actual != [list(row) for row in expected]:
    fail('regional rows differ from independent expected values')

# A second route reconciles the source using integer cents, without summarize.py.
with args.source.open(newline='') as source:
    rows = list(csv.DictReader(source))
source_cents = 0
order_regions = {}
for row in rows:
    price = row['unit_price']
    if not re.fullmatch(r'\d+\.\d{2}', price):
        fail('fixture price must have two decimal places')
    whole, fraction = price.split('.')
    source_cents += int(row['units']) * (100 * int(whole) + int(fraction))
    order_regions.setdefault(row['order_id'], set()).add(row['region'])
if any(len(regions) != 1 for regions in order_regions.values()):
    fail('order spans regions; regional counts cannot be summed')
report_cents = sum(int(row[4].replace('.', '')) for row in actual)
if (sum(int(row[1]) for row in actual) != len(rows)
        or sum(int(row[2]) for row in actual) != len(order_regions)
        or sum(int(row[3]) for row in actual) != sum(int(row['units']) for row in rows)
        or report_cents != source_cents):
    fail('report does not reconcile to source')
print(f'PASS {args.case}: {len(actual)} regions; {len(rows)} lines; {len(order_regions)} orders; {sum(int(row["units"]) for row in rows)} units; {source_cents / 100:.2f} revenue')
