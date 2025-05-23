# docs/tests/test_feature_generator.py.md

# Feature Generator Test Module Documentation

## Overview
This module contains tests for the feature generator functionality in the stock trading application.

## Key Testing Principles

### Static Expected Values
All tests use static, pre-calculated expected values rather than dynamic recalculation within the test. This ensures:

1. **Independent Verification**: The correctness of functions is verified against known good values, not calculated within the test using similar logic to the implementation.
2. **Test Clarity**: The expected outcome is immediately apparent from reading the test.
3. **Regression Detection**: Changes to the implementation that affect output will be caught by tests.
4. **Maintainability**: The expected values are clearly defined in the test, making it easier to understand and maintain.

### Test Coverage
The test suite includes:

- Basic functionality tests for all feature calculation functions
- Edge case handling (empty DataFrames, NaN values, different data types)
- Error handling (invalid parameters, missing columns, etc.)
- Logging verification

### Parameterized Testing
Many tests use `pytest.mark.parametrize` to test multiple scenarios with the same test function, reducing code duplication and ensuring consistent testing across functions.

## Test Functions

### Feature Calculation Basic Tests
- `test_feature_basic`: Tests the basic functionality of all feature calculation functions (SMA, price change percentage, volatility) using parameterized testing.

### Window Size Tests
- `test_window_larger_than_data`: Tests behavior when window size is larger than available data.

### Error Handling Tests
- `test_invalid_column`: Tests error handling when an invalid column is specified.
- `test_invalid_window`: Tests error handling when an invalid window size is specified.
- `test_non_numeric_column`: Tests error handling when a non-numeric column is used.

### Logging Tests
- Various tests with `caplog` to verify correct logging behavior.

### Function-Specific Tests
Detailed tests for each feature calculation function:
- `test_add_sma_*`: Tests for SMA calculation
- `test_add_price_change_pct_1d_*`: Tests for price change percentage
- `test_add_volatility_nday_*`: Tests for volatility

### Feature Generation Tests
- `test_generate_features_*`: Tests for the feature generation orchestrator function.

## Testing Guidelines
When modifying existing tests or adding new ones:

1. Always use static, pre-calculated expected values.
2. Do not recalculate expected values within the test using logic similar to the implementation.
3. Include comprehensive edge case testing.
4. Verify error handling for all expected error conditions.
5. Test logging output for critical operations and error conditions.
