package com.example.orders.pricing;

/** One line of an order: a product code and how many units. */
public record OrderLine(String sku, int units) {
}
