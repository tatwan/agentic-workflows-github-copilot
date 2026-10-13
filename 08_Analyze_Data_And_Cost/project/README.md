# Leaf & Pot orders

Orders from Leaf & Pot, a small online tea shop, for January to March 2026, as exported from the shop.

| Folder | What it holds |
|---|---|
| `data/` | `orders-2026-q1.csv`, one row per order |

| Column | Meaning |
|---|---|
| `order_id` | The order number |
| `date` | The order date, year-month-day |
| `product` | What was ordered; one product per order |
| `quantity` | How many |
| `unit_price` | Price of one, in US dollars |
| `amount` | `quantity` times `unit_price`, in US dollars |
| `status` | `completed` or `cancelled` |

The shop, its products and its orders are fictional.
