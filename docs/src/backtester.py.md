# Module: src/backtester.py

## Overview
This module provides the simulation framework for backtesting trading strategies based on generated signals. It is responsible for simulating trades, tracking portfolio value, and logging trade activity.

## Main Interface
### run_backtest
```
def run_backtest(
    df_with_signals: pd.DataFrame,
    initial_capital: float,
    signal_col: str = 'Signal',
    price_col: str = 'Close'
) -> tuple[list[dict], pd.Series]
```
- **Purpose:** Simulate trading based on signals in the DataFrame.
- **Args:**
    - `df_with_signals`: DataFrame with at least signal and price columns.
    - `initial_capital`: Starting cash for the simulation.
    - `signal_col`: Name of the column with trading signals (default 'Signal').
    - `price_col`: Name of the column with price data (default 'Close').
- **Returns:**
    - `trade_log`: List of trade events (empty for skeleton).
    - `portfolio_values`: Series of portfolio values (empty for skeleton).
- **Raises:**
    - `ValueError`: If required columns are missing.
- **Logging:**
    - Logs when run_backtest is called, using the logger name (from `logging.getLogger(__name__)`) as configured. No manual '[backtester]' prefix is included in the message body; contextual information is provided by the logging framework.

## Current Status
- Only the function skeleton and input validation are implemented. No actual simulation logic yet.

## Next Steps
- Implement portfolio tracking, trade execution, and trade logging in subsequent tasks.
