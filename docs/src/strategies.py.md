<!-- filepath: docs\src\strategies.py.md -->
# `strategies.py` Module Documentation

## Overview
The `src/strategies.py` module is intended to house the various trading strategy implementations for the Simple Stock Strategy Backtester (S3B).

It will define a `BaseStrategy` class from which all specific strategies will inherit, ensuring a common interface for strategy evaluation.

## Current Structure

### `BaseStrategy` Class
- **Purpose:** Serves as the foundational class for all strategy implementations.
- **Attributes:** (To be defined as strategies are developed)
- **Methods:** (To be defined as strategies are developed)

## `generate_sma_crossover_signals` Function

- **Purpose:**
    - Generates trading signals (BUY, SELL, HOLD) based on the crossover of short and long Simple Moving Averages (SMA).
    - Returns a Pandas Series with 1 for BUY, -1 for SELL, and 0 for HOLD at each time step.
- **Parameters:**
    - `data` (`pd.DataFrame`): DataFrame containing at least 'SMA_short' and 'SMA_long' columns.
    - `short_window` (`int`): The short moving average window (for context, not directly used in this function).
    - `long_window` (`int`): The long moving average window (for context, not directly used in this function).
- **Returns:**
    - `pd.Series`: Series of trading signals (1 for BUY, -1 for SELL, 0 for HOLD), named 'signal'.
- **Raises:**
    - `ValueError`: If required columns are missing from the input DataFrame.

### Example Usage
```python
import pandas as pd
from src.strategies import generate_sma_crossover_signals

data = pd.DataFrame({
    'close': [10, 12, 13, 15, 14, 13, 12, 11, 13, 15],
    'SMA_short': [10, 11, 12, 13.5, 14, 13.5, 13, 12, 12.5, 14],
    'SMA_long':  [10, 10.5, 11, 11.5, 12.5, 13, 13.5, 13, 12.5, 12.5]
})
signals = generate_sma_crossover_signals(data, short_window=5, long_window=10)
print(signals)
```

## Future Enhancements
- Implementation of specific strategies (e.g., SMA Crossover, EMA Crossover).
- Methods for signal generation based on strategy logic.
- Parameterization of strategies.
