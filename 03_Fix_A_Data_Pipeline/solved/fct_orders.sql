-- One row per complete order, with its discount and net amount.
-- An order with no row in stg_discounts has a discount of 0.
select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.gross_amount,
    coalesce(d.discount_amount, 0) as discount_amount,
    o.gross_amount - coalesce(d.discount_amount, 0) as net_amount
from {{ ref('stg_orders') }} as o
left join {{ ref('stg_discounts') }} as d on d.order_id = o.order_id
where o.status = 'complete'
