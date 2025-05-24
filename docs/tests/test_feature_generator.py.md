# tests/test_feature_generator.py.md

# Feature Generator Test Module Documentation

## Overview
This file contains tests for the `src/feature_generator.py` module, covering all primary feature engineering functions, error handling, and logging behavior. All tests directly target the primary API functions (add_*) rather than legacy aliases (calculate_*), with separate minimal tests to verify the legacy functions correctly delegate to their primary counterparts.

## Test Structure
- Each primary function (e.g., `add_sma`, `add_price_change_pct_1d`, `add_volatility_nday`) has:
  - A signature test (e.g., `test_add_sma_signature_and_behavior`) that checks only the function signature. Comments in these tests now clarify that behavior, error handling, and logging are covered in dedicated test functions.
  - Dedicated tests for valid inputs, error handling, and logging (e.g., `test_add_sma_with_valid_inputs`, `test_add_sma_raises_appropriate_errors`, `test_sma_logging`).
- The test suite uses static, pre-calculated expected values for independent verification.
- Logging is tested using pytest's `caplog` fixture.

## Recent Documentation Update (2025-05-23)
- Comments in all *_signature_and_behavior tests have been revised to accurately reflect their scope, addressing a minor documentation flaw. These tests now state that they only check the function signature, and that other aspects are covered in dedicated tests.
- Redundant test_calculate_X_logs_error_on_Y functions (e.g., test_calculate_sma_logs_error_on_invalid_column) have been removed. All log message assertions for error conditions are now consolidated in the comprehensive test_X_logging functions (e.g., test_sma_logging, test_price_change_pct_logging, test_volatility_logging), as mandated by the architectural review. This reduces maintenance overhead and ensures all log message checks are in a single, well-documented location for each feature function.

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
- `test_non_numeric_column`: Tests error handling when a non-numeric column is used.
- Error handling for invalid columns and invalid window sizes is tested in the logging tests.

### Logging Tests
- Various tests with `caplog` to verify correct logging behavior.

### Function-Specific Tests
Detailed tests for each feature calculation function:
- `test_add_sma_*`: Tests for SMA calculation
- `test_add_price_change_pct_1d_*`: Tests for price change percentage
- `test_add_volatility_nday_*`: Tests for volatility

### Legacy Function Delegation Tests
- `test_legacy_function_delegation`: Verifies that legacy functions (calculate_*) correctly delegate to their primary API counterparts (add_*).

### Feature Generation Tests
- `test_generate_features_*`: Tests for the feature generation orchestrator function.

## Example: Signature Test
```python
def test_add_sma_signature_and_behavior():
    import inspect
    from src import feature_generator
    sig = inspect.signature(feature_generator.add_sma)
    assert list(sig.parameters.keys()) == ["df", "column", "window"]
    # This test only checks the function signature. Behavior, error handling, and logging are covered in dedicated test functions like test_add_sma_with_valid_inputs, test_add_sma_raises_appropriate_errors, and test_sma_logging.
```

## Test Coverage
- All primary feature engineering functions
- Edge cases (e.g., empty DataFrames, invalid columns, window sizes)
- Logging for error and warning conditions
- Backward-compatibility aliases

## Location
`tests/test_feature_generator.py`

## Testing Guidelines
When modifying existing tests or adding new ones:

1. Always use static, pre-calculated expected values.
2. Do not recalculate expected values within the test using logic similar to the implementation.
3. Include comprehensive edge case testing.
4. Verify error handling for all expected error conditions.
5. Test logging output for critical operations and error conditions.

---
This documentation is up-to-date as of 2025-05-24 and reflects the current structure and scope of the test suite for `src/feature_generator.py`. Content has been consolidated from the misplaced documentation file to ensure consistency and proper location structure.
