# tests/test_metrics.py

## Purpose
Unit tests for `src/metrics.py`. Ensures correctness of all performance metric calculations and output formatting.

## Key Test Functions
- `test_calculate_metrics`: Verifies all metrics (returns, drawdown, Sharpe, etc.)
- `test_print_metrics`: Checks formatted output and partial dict handling.
- `test_edge_cases`: Tests single value, zero-duration, and empty input.

## Coverage
- All supported metrics
- Edge cases and error handling
- Console output formatting

## Notes
- 62+ tests for comprehensive coverage.
- Integration with backtester data structures.
