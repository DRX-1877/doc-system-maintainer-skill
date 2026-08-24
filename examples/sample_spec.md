# Sample Specification (Given-When-Then Reference)

This document provides a standard BDD specification reference for AI agents.

## Feature Specification: DEMO-001 Coupon Discount Calculation

### 1. Business Context
Users should be able to apply valid promotional coupons to deduct order subtotals.

### 2. Acceptance Criteria (BDD)

#### Scenario 1: Successful Coupon Application (Happy Path)
- **Given** User owns a coupon with $10 discount valid for orders over $50
- **When** User submits an order with items total of $60 and selects this coupon
- **Then** System deducts $10 from final amount and responds with HTTP `201 Created`.

#### Scenario 2: Subtotal Below Threshold (Unhappy Path)
- **Given** Order items total is $40
- **When** User attempts to apply a coupon requiring a minimum spend of $50
- **Then** System responds with HTTP `400 Bad Request` and error detail "Minimum order amount not met".
