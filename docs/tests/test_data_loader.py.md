# tests/test_data_loader.py

## Overview
This file contains tests for the data loading functionality in `src/data_loader.py`. The tests focus on verifying the behavior of the primary `fetch_data` function, with minimal testing of the backward-compatibility wrapper `fetch` function.

## Testing Approach
The test suite follows these key principles:

1. **DRY (Don't Repeat Yourself):** To avoid code duplication, comprehensive tests are written only for the primary `fetch_data` function. The `fetch` function, being a thin wrapper around `fetch_data`, is tested only for proper delegation.

2. **Mocking External Dependencies:** All tests use mocks for the `yfinance` library to avoid network calls and ensure consistent test behavior.

3. **Independence from External Services:** Tests do not depend on external APIs, except for optional integration tests which are skipped by default.

4. **Coverage of Edge Cases:** Tests include parameter validation, error handling, caching behavior, and column filtering.

## Test Functions

### Primary Function Tests (for `fetch_data`)
- `test_fetch_data_calls_yfinance_and_returns_dataframe`: Verifies that `fetch_data` calls yfinance with the correct ticker and returns a properly structured DataFrame.
- `test_fetch_data_validates_ticker`: Confirms that `fetch_data` validates the ticker parameter.
- `test_fetch_data_validates_period`: Ensures period parameter validation.
- `test_fetch_data_validates_columns`: Verifies column validation against returned data.
- `test_fetch_data_parameterized_columns`: Tests column selection functionality.
- `test_fetch_data_caching`: Confirms that the caching mechanism works as expected.
- `test_fetch_data_handles_yfinance_error`: Ensures proper error handling for yfinance exceptions.
- `test_fetch_data_handles_empty_data`: Verifies handling of empty DataFrame returns.
- `test_fetch_data_all_nan_column`: Tests detection and handling of all-NaN columns.
- `test_fetch_data_logs_error_on_invalid_input`: Confirms proper error logging.

### Wrapper Function Tests (for `fetch`)
- `test_fetch_delegates_to_fetch_data`: Verifies that `fetch` properly delegates to `fetch_data` with the correct parameters, focusing specifically on the wrapper behavior.

### Integration Tests
- `test_fetch_data_integration_real_api`: An integration test that uses the real yfinance API (skipped by default).

## Testing Best Practices
- Always verify function behavior through assertions, not just test for exceptions.
- When mocking, ensure the mock structure matches the expected return value structure.
- Keep test function names descriptive of what they are testing.
- Use the `@pytest.mark.skip` decorator with clear reasons for any skipped tests.
- When testing backward-compatibility wrappers, only test the delegation behavior, not the full functionality which should be covered by tests for the primary function.
