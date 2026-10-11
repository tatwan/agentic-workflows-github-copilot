select
    order_id,
    customer_id,
    cast(order_date as date) as order_date,
    status,
    cast(gross_amount as decimal(10, 2)) as gross_amount
from {{ ref('raw_orders') }}
