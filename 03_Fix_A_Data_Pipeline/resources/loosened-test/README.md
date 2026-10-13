# A fix that loosened the tests

This is the quickest way to turn the build green: tell the two failing tests to warn instead of fail. We wrote it
for this lab; it is not a recorded Copilot run, but it is a change an agent can make when the request only says
"make the build pass".

| File | What it is |
|---|---|
| `schema.yml` | The project's tests with two changes, below. `fct_orders.sql` is unchanged |
| `build-output.txt` | What `uv run dbt build` printed |
| `rows-output.txt` | What `dbt show` printed afterwards |

## What changed

```diff
       - name: discount_amount
         description: The order's discount.
-        data_tests: [not_null]
+        data_tests:
+          - not_null:
+              config:
+                severity: warn  # orders without a discount have no discount row
```

The test on `net_amount` got the same `severity: warn`. The comment sounds reasonable, and it is true of the
discounts table. It is not true of `fct_orders`, where every order needs a discount and a net amount, even if the
discount is 0.

## What the build said

```text
Completed with 2 warnings:

[WARNING]: in test not_null_fct_orders_discount_amount (models/schema.yml)
[WARNING]: Got 24 results, configured to warn if != 0
...
Done. PASS=17 WARN=2 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=19
```

A warning does not stop a build, so the command succeeds. The two tests still find the same 24 rows; they are
just no longer allowed to fail.

## What finance got

| orders | with_net | net_total |
|---:|---:|---:|
| 35 | 11 | 2,120.1 |

Order 1 is in the table with an empty discount and an empty net amount. 24 of the 35 complete orders have no net
amount, so a net sales total adds up 11 orders: 2,120.10 instead of 6,417.95.

## How you catch it

- **The changed files.** `models/schema.yml` is on the list. The request said only `fct_orders.sql` may change.
- **The rows.** 11 of 35 orders have a net amount, and order 1's is empty.
