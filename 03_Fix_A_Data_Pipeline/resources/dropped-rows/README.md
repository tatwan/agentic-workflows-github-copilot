# A fix that dropped the rows

This build changes only `fct_orders.sql`, and every test passes. We wrote it for this lab; it is not a recorded
Copilot run.

| File | What it is |
|---|---|
| `fct_orders.sql` | The model with one word changed: `inner join` instead of `left join` |
| `build-output.txt` | What `uv run dbt build` printed |
| `rows-output.txt` | What `dbt show` printed afterwards |

## What changed

```diff
 from {{ ref('stg_orders') }} as o
-left join {{ ref('stg_discounts') }} as d on d.order_id = o.order_id
+inner join {{ ref('stg_discounts') }} as d on d.order_id = o.order_id
 where o.status = 'complete'
```

A left join keeps every order and leaves the discount empty when there is none. An inner join keeps only the orders
that have a row in both tables. The 24 complete orders without a discount leave the table, and with them every
empty value the tests were finding.

## What the build said

```text
Done. PASS=19 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=19
```

This is the same line a correct fix prints. Nineteen checks, all passing, on a table that lost two thirds of its
rows.

## What finance got

| orders | with_net | net_total |
|---:|---:|---:|
| 11 | 11 | 2,120.1 |

Order 1 is not in the table at all. Net sales come to 2,120.10 instead of 6,417.95.

## How you catch it

- **The changed files** do not help: only `fct_orders.sql` changed, as the request allowed.
- **The tests** do not help: `not_null` checks the rows that are there, not the rows that are missing.
- **The rows** do: 11 where you expected 35, and no order 1.

To make this check part of the build, see the lab's challenge 2.
