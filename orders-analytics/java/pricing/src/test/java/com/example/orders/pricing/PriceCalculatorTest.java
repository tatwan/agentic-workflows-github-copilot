package com.example.orders.pricing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;

class PriceCalculatorTest {

    private final PriceCalculator calculator = new PriceCalculator();

    @Test
    void lineTotalIsUnitPriceTimesUnits() {
        assertEquals(new BigDecimal("42.00"), calculator.lineTotal(new OrderLine("NB-A5", 12)));
    }

    @Test
    void lineTotalRoundsHalfEvenToTwoPlaces() {
        assertEquals(new BigDecimal("0.38"), calculator.lineTotal(new OrderLine("LBL-1", 3)));
        assertEquals(new BigDecimal("0.62"), calculator.lineTotal(new OrderLine("LBL-1", 5)));
    }

    @Test
    void orderTotalRoundsOnceAtTheEnd() {
        List<OrderLine> lines = List.of(new OrderLine("LBL-1", 3), new OrderLine("LBL-1", 3));
        assertEquals(new BigDecimal("0.75"), calculator.orderTotal(lines));
    }

    @Test
    void unknownSkuIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> calculator.lineTotal(new OrderLine("NOPE", 1)));
    }

    @Test
    void unitsMustBePositive() {
        assertThrows(IllegalArgumentException.class, () -> calculator.lineTotal(new OrderLine("NB-A5", 0)));
    }
}
