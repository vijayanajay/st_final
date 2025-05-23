# `strategies.py` Module Documentation

## Overview
The `src/strategies.py` module houses the various trading strategy implementations for the Simple Stock Strategy Backtester (S3B). It implements the Strategy Pattern where different trading strategies inherit from a common `BaseStrategy` abstract base class.

## Current Structure

### `BaseStrategy` Class
- **Purpose:** Serves as the foundational abstract class for all strategy implementations.
- **Interface Methods:**
  - `generate_signals(df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series`: Abstract method that all strategies must implement to generate trading signals.
  - `get_required_parameters() -> List[str]`: Abstract method that returns a list of required parameters for the strategy.
  - `validate_parameters(params: Dict[str, Any]) -> None`: Validates that all required parameters are present.

### `SMACrossoverStrategy` Class
- **Purpose:** Implements the SMA crossover strategy that inherits from `BaseStrategy`.
- **Required Parameters:**
  - `fast_sma`: Column name for the short-term SMA.
  - `slow_sma`: Column name for the long-term SMA.
- **Signal Logic:**
  - **BUY (1)**: When the short SMA crosses above the long SMA.
  - **SELL (-1)**: When the short SMA crosses below the long SMA.
  - **HOLD (0)**: No crossover event.

### `STRATEGY_REGISTRY` Dictionary
- **Purpose:** Maps strategy type strings to strategy classes for dynamic instantiation.
- **Current Entries:**
  - `'sma_crossover'`: Maps to `SMACrossoverStrategy`.

### `generate_sma_crossover_signals` Function

- **Purpose:**
    - Generates trading signals (BUY, SELL, HOLD) based on the crossover of short and long Simple Moving Averages (SMA).
    - Returns a Pandas Series with 1 for BUY, -1 for SELL, and 0 for HOLD at each time step.
    - **Note:** Maintained for backward compatibility. New code should use the `SMACrossoverStrategy` class directly.
- **Parameters:**
    - `df_with_features` (`pd.DataFrame`): DataFrame containing SMA feature columns.
    - `short_window_col` (`str`, optional): Name of the short window SMA column. Defaults to "SMA_short".
    - `long_window_col` (`str`, optional): Name of the long window SMA column. Defaults to "SMA_long".
- **Returns:**
    - `pd.Series`: Series of trading signals (1 for BUY, -1 for SELL, 0 for HOLD), named 'signal'.
- **Raises:**
    - `ValueError`: If required columns are missing from the input DataFrame.

#### Testing
The following tests for `generate_sma_crossover_signals` are implemented in `tests/test_strategies.py`:
- Basic SMA crossover signal generation for BUY, SELL, and HOLD scenarios.
- Signature and behavior validation (parameter names, return type).
- Handling of NaN values in SMA columns (should result in HOLD/0 signals).
- All values equal (no crossovers, all HOLD).
- No crossovers (short SMA always above or below long SMA).
- Empty DataFrame (should return empty signal series).
- DataFrame shorter than signal period (should be all HOLD).
- Signal at edges (crossovers at the very beginning or end of the data).

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

**Note on Design Evolution:**
The implementation has evolved to follow the Strategy Pattern as described in the architectural documentation. The `generate_sma_crossover_signals` function is now a wrapper around the `SMACrossoverStrategy` class for backward compatibility.

## Signal Logic

The signal generation logic in `SMACrossoverStrategy` follows these crossover rules:
- **BUY (1)**: When the short SMA crosses above the long SMA
- **SELL (-1)**: When the short SMA crosses below the long SMA
- **HOLD (0)**: No crossover event

The crossover is specifically defined as:
- **BUY**: `(short_sma.shift(1) <= long_sma.shift(1)) & (short_sma > long_sma)`
- **SELL**: `(short_sma.shift(1) >= long_sma.shift(1)) & (short_sma < long_sma)`

This ensures signals are only generated at the actual crossover points, not continuously while one SMA is above or below the other.

## Using the Strategy Pattern

### Example: Using SMACrossoverStrategy directly
```python
import pandas as pd
from src.strategies import SMACrossoverStrategy

# Create data with SMA columns
data = pd.DataFrame({
    'close': [10, 12, 13, 15, 14, 13, 12, 11, 13, 15],
    'SMA5': [10, 11, 12, 13.5, 14, 13.5, 13, 12, 12.5, 14],
    'SMA10': [10, 10.5, 11, 11.5, 12.5, 13, 13.5, 13, 12.5, 12.5]
})

# Create strategy instance
strategy = SMACrossoverStrategy()

# Define parameters
params = {
    'fast_sma': 'SMA5',
    'slow_sma': 'SMA10'
}

# Generate signals
signals = strategy.generate_signals(data, params)
print(signals)
```

### Example: Using apply_strategy with Strategy Pattern
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

### Creating a New Strategy

To add a new strategy:

1. Create a new class that inherits from `BaseStrategy`
2. Implement the required abstract methods:
   - `generate_signals(df, params)`: Implement the signal generation logic
   - `get_required_parameters()`: Return a list of parameter names required by the strategy
3. Add the new strategy to the `STRATEGY_REGISTRY` dictionary:
   ```python
   STRATEGY_REGISTRY['new_strategy_name'] = NewStrategyClass
   ```

Example:
```python
class RSIStrategy(BaseStrategy):
    def get_required_parameters(self) -> List[str]:
        return ['rsi_column', 'overbought_level', 'oversold_level']
        
    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        self.validate_parameters(params)
        # Strategy implementation here
        # ...
        return signals

# Add to registry
STRATEGY_REGISTRY['rsi'] = RSIStrategy
```

## `apply_strategy` Function

- **Purpose:**
    - Applies a trading strategy to a DataFrame and generates buy/sell signals.
    - Uses the Strategy pattern to dynamically instantiate and use strategy objects.
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

#### Testing
The following tests for `apply_strategy` are implemented in `tests/test_apply_strategy.py`:
- Correct signal generation for SMA crossover strategy (known crossover points).
- Proper handling of valid and invalid `strategy_params` (missing keys, incorrect types).
- Behavior with different fast_sma and slow_sma column names.
- Error handling for unsupported strategy types.
- Edge cases: empty DataFrame, DataFrame with NaNs in feature columns.
- Logging behavior (verifies expected log messages).
- Preservation of the original DataFrame (no in-place modification).

### Example Usage
```python
import pandas as pd
from src.strategies import apply_strategy

# Sample data
df = pd.DataFrame({
    'close': [100, 102, 101, 105, 107],
    'SMA_short': [100, 101, 102, 103, 104],
    'SMA_long': [100, 100.5, 101, 101.5, 102]
})

# Strategy parameters
params = {
    'strategy_type': 'sma_crossover',
    'parameters': {
        'fast_sma': 'SMA_short',
        'slow_sma': 'SMA_long'
    }
}

# Apply strategy
df_with_signals = apply_strategy(df, params)
print(df_with_signals)
```

## Logging

- **Purpose:** Provides logging functionality for the module, especially for strategy signal generation.
- **Logging Levels:** Uses DEBUG level for detailed internal state logging, INFO for general messages, and ERROR for exception cases.
- **Log Messages:** Includes messages for:
  - Strategy initialization
  - Signal generation process start and end
  - Parameter validation results
  - Crossover detection for signals
  - Errors and exceptions

### Example Log Output
```
DEBUG:root:Initializing SMACrossoverStrategy with parameters: {'fast_sma': 'SMA5', 'slow_sma': 'SMA10'}
INFO:root:Generating signals using SMACrossoverStrategy
DEBUG:root:Validating parameters: {'fast_sma': 'SMA5', 'slow_sma': 'SMA10'}
DEBUG:root:Parameters valid: {'fast_sma': 'SMA5', 'slow_sma': 'SMA10'}
DEBUG:root:Signal generation complete. Sample signals:
0    0
1    0
2    1
3    0
4   -1
Name: signal, dtype: int64
```

## Testing

The module includes comprehensive tests in:
- `tests/test_strategies.py`: Tests for the `generate_sma_crossover_signals` function.
- `tests/test_apply_strategy.py`: Tests for the `apply_strategy` function.
- `tests/test_strategy_pattern.py`: Tests for the Strategy pattern implementation, including `BaseStrategy`, `SMACrossoverStrategy`, and the strategy registry.

### Running Tests
To run the tests:
1. Ensure the test files are present in the `tests` directory.
2. Run the following command in the terminal:
   ```bash
   pytest --tb=short -q tests/test_strategies.py tests/test_apply_strategy.py tests/test_strategy_pattern.py
   ```
3. Review the test output for any failures or errors.
