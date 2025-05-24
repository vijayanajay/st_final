# tests/test_strategies.py

## Purpose
Unit tests for `src/strategies.py`. Focuses on the `BaseStrategy` class and `generate_sma_crossover_signals` function.

## Key Test Functions
- `test_base_strategy_abstract_methods`: Ensures abstract methods enforce implementation.
- `test_generate_sma_crossover_signals`: Verifies correct signal generation and error handling.

## Coverage
- Abstract base class enforcement
- SMA crossover logic
- Error handling for missing columns

## Notes
- Uses pandas DataFrames for test data.
- Maintains backward compatibility with legacy signal functions.
