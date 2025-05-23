# tests/test_feature_generator.py.md

## Overview
This file contains tests for the `src/feature_generator.py` module, covering all primary feature engineering functions, error handling, and logging behavior.

## Test Structure
- Each primary function (e.g., `add_sma`, `add_price_change_pct_1d`, `add_volatility_nday`) has:
  - A signature test (e.g., `test_add_sma_signature_and_behavior`) that checks only the function signature. Comments in these tests now clarify that behavior, error handling, and logging are covered in dedicated test functions.
  - Dedicated tests for valid inputs, error handling, and logging (e.g., `test_add_sma_with_valid_inputs`, `test_add_sma_raises_appropriate_errors`, `test_sma_logging`).
- The test suite uses static, pre-calculated expected values for independent verification.
- Logging is tested using pytest's `caplog` fixture.

## Recent Documentation Update (2025-05-23)
- Comments in all *_signature_and_behavior tests have been revised to accurately reflect their scope, addressing a minor documentation flaw. These tests now state that they only check the function signature, and that other aspects are covered in dedicated tests.
- Redundant test_calculate_X_logs_error_on_Y functions (e.g., test_calculate_sma_logs_error_on_invalid_column) have been removed. All log message assertions for error conditions are now consolidated in the comprehensive test_X_logging functions (e.g., test_sma_logging, test_price_change_pct_logging, test_volatility_logging), as mandated by the architectural review. This reduces maintenance overhead and ensures all log message checks are in a single, well-documented location for each feature function.

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

---
This documentation is up-to-date as of 2025-05-23 and reflects the current structure and scope of the test suite for `src/feature_generator.py`.
