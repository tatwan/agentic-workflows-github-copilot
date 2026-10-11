-- Running value of complete orders per customer, in date order.
-- Used by Labs 03 and 05. Review it; do not edit it in place.
SELECT
    c.customer_id,
    c.region,
    o.order_id,
    o.order_date,
    (
        SELECT sum(li2.quantity * li2.unit_price)
        FROM orders AS o2
        JOIN line_items AS li2 ON li2.order_id = o2.order_id
        WHERE o2.customer_id = o.customer_id
          AND o2.status = 'complete'
          AND o2.order_date <= o.order_date
    ) AS running_value
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.status = 'complete'
ORDER BY c.customer_id, o.order_date, o.order_id;
