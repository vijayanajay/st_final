# tests/test_apply_strategy.py

## Purpose
Unit tests for the `apply_strategy` function in `src/strategies.py`. Ensures correct application of trading strategies to DataFrames.

## Key Test Functions
- `test_apply_strategy_valid_params`: Verifies correct signal generation for valid parameters.
- `test_apply_strategy_invalid_params`: Checks error handling for missing/invalid parameters.
- `test_apply_strategy_edge_cases`: Tests empty DataFrames and NaN handling.
- Logging tests: Ensures appropriate log messages.

## Coverage
- Strategy type validation
- Parameter validation
- Data integrity and error handling

## Notes
- Tests preservation of input DataFrame.
- Extensible for new strategy types.
