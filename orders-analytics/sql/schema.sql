-- Orders analytics schema (DuckDB). Synthetic, course-authored.
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        VARCHAR NOT NULL,
    region      VARCHAR NOT NULL,   -- North, South, East, West
    segment     VARCHAR NOT NULL    -- retail, wholesale, online
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    order_date  DATE    NOT NULL,
    status      VARCHAR NOT NULL    -- complete, cancelled, pending
);

CREATE TABLE line_items (
    order_id    INTEGER NOT NULL REFERENCES orders (order_id),
    line_no     INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL,
    unit_price  DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, line_no)
);
