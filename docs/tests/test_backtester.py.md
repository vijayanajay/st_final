# tests/test_backtester.py

## Purpose
Unit tests for `src/backtester.py`. Verifies correctness of backtesting simulation, trade execution, and portfolio tracking.

## Key Test Functions
- `test_run_backtest_basic`: Tests basic trade simulation and portfolio value calculation.
- `test_run_backtest_enhanced`: Verifies enhanced analytics and PortfolioData structure.
- `test_edge_cases`: Handles empty signals, NaNs, and invalid input.

## Coverage
- Trade execution logic
- Portfolio value and analytics
- Error handling and logging

## Notes
- Uses sample DataFrames for reproducibility.
- Extensible for new backtesting features.
