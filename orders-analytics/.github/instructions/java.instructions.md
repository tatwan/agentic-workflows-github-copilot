---
applyTo: "java/pricing/**/*.java"
description: Java rules for the pricing module
---
- Money is BigDecimal, never double
- Round half-even to 2 places, once, at the end
