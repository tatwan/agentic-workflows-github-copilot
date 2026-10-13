-- Every complete order in stg_orders has a row in fct_orders.
-- Returns the complete orders that are missing; the test fails if there are any.
select o.order_id
from {{ ref('stg_orders') }} as o
left join {{ ref('fct_orders') }} as f on f.order_id = o.order_id
where o.status = 'complete'
  and f.order_id is null
