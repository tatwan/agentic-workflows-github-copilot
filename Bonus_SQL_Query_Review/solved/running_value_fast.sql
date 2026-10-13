-- Running value of complete orders per customer, in date order.
-- Rewrite: add up each order once, then keep a running total per customer.
WITH order_values AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        sum(li.quantity * li.unit_price) AS order_value
    FROM orders AS o
    JOIN line_items AS li ON li.order_id = o.order_id
    WHERE o.status = 'complete'
    GROUP BY o.order_id, o.customer_id, o.order_date
)
SELECT
    c.customer_id,
    c.region,
    v.order_id,
    v.order_date,
    sum(v.order_value) OVER (
        PARTITION BY v.customer_id
        ORDER BY v.order_date
        RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_value
FROM order_values AS v
JOIN customers AS c ON c.customer_id = v.customer_id
ORDER BY c.customer_id, v.order_date, v.order_id;
