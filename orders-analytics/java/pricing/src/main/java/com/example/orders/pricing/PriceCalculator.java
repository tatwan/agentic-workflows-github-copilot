package com.example.orders.pricing;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import java.util.Map;

/** Prices order lines from a catalogue of unit prices. */
public final class PriceCalculator {

    private final Map<String, BigDecimal> unitPrices;

    public PriceCalculator(Map<String, BigDecimal> unitPrices) {
        this.unitPrices = Map.copyOf(unitPrices);
    }

    public PriceCalculator() {
        this(UnitPrices.CATALOGUE);
    }

    /** Unit price times units, rounded half-even to 2 places. */
    public BigDecimal lineTotal(OrderLine line) {
        return rawLineTotal(line).setScale(2, RoundingMode.HALF_EVEN);
    }

    /** Sum of the lines, rounded half-even to 2 places once, at the end. */
    public BigDecimal orderTotal(List<OrderLine> lines) {
        BigDecimal total = BigDecimal.ZERO;
        for (OrderLine line : lines) {
            total = total.add(rawLineTotal(line));
        }
        return total.setScale(2, RoundingMode.HALF_EVEN);
    }

    private BigDecimal rawLineTotal(OrderLine line) {
        if (line.units() <= 0) {
            throw new IllegalArgumentException("units must be positive: " + line.units());
        }
        BigDecimal price = unitPrices.get(line.sku());
        if (price == null) {
            throw new IllegalArgumentException("unknown sku: " + line.sku());
        }
        return price.multiply(BigDecimal.valueOf(line.units()));
    }
}
