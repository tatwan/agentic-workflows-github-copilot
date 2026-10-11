package com.example.orders.pricing;

import java.math.BigDecimal;

/**
 * Shipping fee for an order: free from 50.00, otherwise a flat 4.95.
 * This class has no tests yet: Lab 10's developer challenge asks you to add them.
 */
public final class ShippingFee {

    static final BigDecimal FREE_FROM = new BigDecimal("50.00");
    static final BigDecimal FLAT_FEE = new BigDecimal("4.95");

    private ShippingFee() {
    }

    /** The fee for an order with this goods total (after any discount). */
    public static BigDecimal forOrderTotal(BigDecimal orderTotal) {
        if (orderTotal.signum() < 0) {
            throw new IllegalArgumentException("order total must not be negative: " + orderTotal);
        }
        if (orderTotal.compareTo(FREE_FROM) >= 0) {
            return BigDecimal.ZERO.setScale(2);
        }
        return FLAT_FEE;
    }
}
