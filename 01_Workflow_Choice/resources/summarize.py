"""Fixed procedure: group order lines by region with exact decimal money."""
import argparse
import csv
from decimal import Decimal
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
if not args.source.is_file():
    parser.exit(1, 'FAIL source CSV not found\n')

groups = {}
with args.source.open(newline='') as source:
    for row in csv.DictReader(source):
        region = row['region']
        if region not in groups:
            groups[region] = {'lines': 0, 'orders': set(), 'units': 0, 'revenue': Decimal('0')}
        group = groups[region]
        units = int(row['units'])
        group['lines'] += 1
        group['orders'].add(row['order_id'])
        group['units'] += units
        group['revenue'] += units * Decimal(row['unit_price'])

args.output.parent.mkdir(parents=True, exist_ok=True)
with args.output.open('w', newline='') as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['region', 'lines', 'orders', 'units', 'revenue'])
    for region in sorted(groups):
        group = groups[region]
        writer.writerow([region, group['lines'], len(group['orders']), group['units'], f"{group['revenue']:.2f}"])
print(args.output.read_text(), end='')
