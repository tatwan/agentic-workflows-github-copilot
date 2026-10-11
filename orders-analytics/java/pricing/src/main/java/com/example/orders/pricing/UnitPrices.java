package com.example.orders.pricing;

import java.math.BigDecimal;
import java.util.Map;

/** Fixed unit prices for the course's fictional catalogue. */
public final class UnitPrices {

    public static final Map<String, BigDecimal> CATALOGUE = Map.of(
            "NB-A5", new BigDecimal("3.50"),     // notebook
            "PEN-10", new BigDecimal("4.25"),    // pen pack
            "LAMP-1", new BigDecimal("24.00"),   // desk lamp
            "LBL-1", new BigDecimal("0.125"));   // label, priced per label

    private UnitPrices() {
    }
}
