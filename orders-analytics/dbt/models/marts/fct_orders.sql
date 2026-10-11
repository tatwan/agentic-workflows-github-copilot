-- One row per complete order.
select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.gross_amount
from {{ ref('stg_orders') }} as o
where o.status = 'complete'
