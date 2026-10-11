-- Setup check for Lab 00: one row per table with its row count.
SELECT 'customers' AS table_name, count(*) AS row_count FROM customers
UNION ALL
SELECT 'orders', count(*) FROM orders
UNION ALL
SELECT 'line_items', count(*) FROM line_items
UNION ALL
SELECT 'slow_orders.sql rows', count(*) FROM orders WHERE status = 'complete';
