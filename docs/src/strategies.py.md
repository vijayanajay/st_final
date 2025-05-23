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
    - `df_with_features` (`pd.DataFrame`): DataFrame containing SMA feature columns.
    - `short_window_col` (`str`, optional): Name of the short window SMA column. Defaults to "SMA_short".
    - `long_window_col` (`str`, optional): Name of the long window SMA column. Defaults to "SMA_long".
- **Returns:**
    - `pd.Series`: Series of trading signals (1 for BUY, -1 for SELL, 0 for HOLD), named 'signal'.
- **Raises:**
    - `ValueError`: If required columns are missing from the input DataFrame.

### Example Usage
```python
import pandas as pd
from src.strategies import generate_sma_crossover_signals

# Example with default column names
data = pd.DataFrame({
    'close': [10, 12, 13, 15, 14, 13, 12, 11, 13, 15],
    'SMA_short': [10, 11, 12, 13.5, 14, 13.5, 13, 12, 12.5, 14],
    'SMA_long':  [10, 10.5, 11, 11.5, 12.5, 13, 13.5, 13, 12.5, 12.5]
})
signals = generate_sma_crossover_signals(data)
print(signals)

# Example with custom column names
data = pd.DataFrame({
    'close': [10, 12, 13, 15, 14, 13, 12, 11, 13, 15],
    'sma_5': [10, 11, 12, 13.5, 14, 13.5, 13, 12, 12.5, 14],
    'sma_20':  [10, 10.5, 11, 11.5, 12.5, 13, 13.5, 13, 12.5, 12.5]
})
signals = generate_sma_crossover_signals(data, short_window_col='sma_5', long_window_col='sma_20')
print(signals)
```

---

**Note on Design Deviation:**
The implementation of `generate_sma_crossover_signals` differs slightly from the specification in `docs/design.md` (Section 4.5):
- It returns a `pd.Series` (named 'signal') instead of a `pd.DataFrame`, as a Series is more direct for a single signal column.
- The `short_window_col` and `long_window_col` parameters have default values, making them optional for convenience, whereas the design listed them as mandatory.

These changes were made for practical implementation benefits and are reflected in the function's documentation and usage examples above.

## Signal Logic

The function generates signals based on the following crossover rules:
- **BUY (1)**: When the short SMA crosses above the long SMA
- **SELL (-1)**: When the short SMA crosses below the long SMA
- **HOLD (0)**: No crossover event

The crossover is specifically defined as:
- **BUY**: `(short_sma.shift(1) <= long_sma.shift(1)) & (short_sma > long_sma)`
- **SELL**: `(short_sma.shift(1) >= long_sma.shift(1)) & (short_sma < long_sma)`

This ensures signals are only generated at the actual crossover points, not continuously while one SMA is above or below the other.

## Future Enhancements
- Implementation of specific strategies (e.g., SMA Crossover, EMA Crossover).
- Methods for signal generation based on strategy logic.
- Parameterization of strategies.

## `apply_strategy` Function

- **Purpose:**
    - Applies a trading strategy to a DataFrame and generates buy/sell signals.
    - Acts as a utility function that can apply different strategy types based on parameters.
- **Parameters:**
    - `df` (`pd.DataFrame`): DataFrame containing price data and any required technical indicators.
    - `strategy_params` (`dict`): Dictionary containing strategy type and parameters. Must include 'strategy_type' key and 'parameters' dict.
- **Returns:**
    - `pd.DataFrame`: Original DataFrame with added 'signal' column (1 = buy, -1 = sell, 0 = no action)
- **Raises:**
    - `ValueError`: If strategy type is not supported or required parameters are missing.

### Supported Strategy Types:
- `sma_crossover`: Generates signals when fast SMA crosses above/below slow SMA
  - Required parameters: 'fast_sma' (column name), 'slow_sma' (column name)

### Example Usage
```python
import pandas as pd
from src.strategies import apply_strategy

# Prepare data with technical indicators
df = pd.DataFrame({
    'Close': [100, 102, 104, 103, 101],
    'SMA5': [101, 102, 103, 102.5, 102],
    'SMA20': [100, 100.5, 101, 101.5, 102]
})

# Define strategy parameters
strategy_params = {
    'strategy_type': 'sma_crossover',
    'parameters': {
        'fast_sma': 'SMA5',
        'slow_sma': 'SMA20'
    }
}

# Apply strategy
result = apply_strategy(df, strategy_params)
print(result)
```

### Testing
The `apply_strategy` function is thoroughly tested in `tests/test_apply_strategy.py` with the following test cases:

1. **Basic functionality**: Tests correct signal generation for the SMA crossover strategy.
2. **Invalid strategy type**: Tests proper error handling for unsupported strategy types.
3. **Missing parameters**: Tests proper error handling when required parameters are missing.
4. **Different column names**: Tests correct behavior when using non-default column names for SMAs.
5. **Empty DataFrame**: Tests handling of an empty DataFrame.
6. **NaNs in feature columns**: Tests proper handling of NaN values in SMA columns.
7. **Logging verification**: Tests that appropriate log messages are generated.
8. **Original DataFrame preservation**: Tests that the original DataFrame is not modified.

These tests ensure the reliability and correctness of the strategy application logic, providing confidence in backtesting results.

### Testing
The `generate_sma_crossover_signals` function is thoroughly tested in `tests/test_strategies.py` with the following test cases:

1. **Basic functionality**: Tests correct signal generation for BUY, SELL, and HOLD scenarios.
2. **NaNs in SMA columns**: Tests proper handling of NaN values in short and long SMA columns.
3. **Always-equal SMAs**: Tests when short and long SMAs are always equal (no crossovers).
4. **No crossovers**: Tests when one SMA is always greater than the other (no crossovers).
5. **Empty DataFrame**: Tests handling of an empty DataFrame.
6. **Very short DataFrame**: Tests DataFrame shorter than any potential signal period (should be all HOLD).
7. **Signals at edges**: Tests if signals can occur at the very beginning or end of the DataFrame.

All tests use static, pre-calculated expected values and `pd.testing.assert_series_equal` for robust comparison. These tests ensure the reliability and correctness of the core signal generation logic, providing confidence in backtesting results.
