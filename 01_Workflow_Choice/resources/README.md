# Lab 01 resources

The CSVs are synthetic, authored for this repository, under its [MIT licence](../../LICENSE). Snapshot:
11 Oct 2026. orders.csv preserves the first eight lines of python/data/orders.csv, including repeated order
IDs; challenge.csv adds a North line and changes the first quantity from four to five. No real customer data.
Revenue is units multiplied by unit_price; no tax, discounts or date selection apply.

summarize.py is a fixed Decimal procedure. check_report.py was written from hand calculations and reconciles
using integer cents, without importing the script. Its core and challenge references are separate. Keep it
outside the project’s normal context. Opening a smaller folder does not enforce a filesystem restriction.
wrong-split.csv is a prepared failure fixture, not an observed model answer. boundary-change.patch is preserved
from the earlier Lab 01 for later engineering work; it is not used by this exercise.

The supplied-context profile has an empty tools list. Its filename describes a Copilot custom role; the lab’s
classification depends on its actual available tools and observed calls. A read-only role that searches files
belongs in the agent comparison. Verify profile discovery and tool scope before treating a response as the
assistance baseline. The prompts keep the same output contract for both model workflows.
