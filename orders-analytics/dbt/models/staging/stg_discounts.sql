-- One row per discounted order. Orders without a discount have no row here.
select
    order_id,
    discount_code,
    cast(discount_amount as decimal(10, 2)) as discount_amount
from {{ ref('raw_discounts') }}
