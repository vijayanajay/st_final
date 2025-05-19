# src/feature_generator.py.md

# Feature Generator Module Documentation

## Overview
This module provides feature engineering utilities for stock trading, including calculation of Simple Moving Averages (SMA).

## Functions

### calculate_sma

**Signature:**
```python
def calculate_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
```

**Description:**
Calculates the Simple Moving Average (SMA) for a specified column in a pandas DataFrame.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame containing price data.
- `column` (str): Name of the column to calculate SMA on.
- `window` (int): Window size for the moving average. Must be > 0.

**Returns:**
- `pd.Series`: Series containing the SMA values, named as 'sma_{window}'.

**Raises:**
- `ValueError`: If the column does not exist or window is invalid.

**Notes:**
- Input validation and error handling are performed, with structured logging for all error conditions and critical operations (see code for logging details).
- Logging is handled using the standard library `logging` module, with configuration centralized in `configs/logging_config.py`.
- The function is tested in `tests/test_feature_generator.py`.

**Example:**
```python
import pandas as pd
from src.feature_generator import calculate_sma

df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
sma = calculate_sma(df, column='close', window=3)
print(sma)
```

---

### calculate_price_change_pct

**Signature:**
```python
def calculate_price_change_pct(df: pd.DataFrame, column: str = "close") -> pd.Series:
```

**Description:**
Calculates the 1-day price change percentage for a specified column in a pandas DataFrame. The result is `(current - previous) / previous * 100` for each row.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame containing price data.
- `column` (str, optional): Name of the column to calculate price change percentage on. Defaults to 'close'.

**Returns:**
- `pd.Series`: Series containing the 1-day price change percentage, named as 'price_change_pct_1d'.

**Raises:**
- `ValueError`: If the column does not exist or is not numeric.

**Notes:**
- Input validation and error handling are performed, with structured logging for all error conditions and critical operations (see code for logging details).
- Logging is handled using the standard library `logging` module, with configuration centralized in `configs/logging_config.py`.
- The function is tested in `tests/test_feature_generator.py`.

**Example:**
```python
import pandas as pd
from src.feature_generator import calculate_price_change_pct

df = pd.DataFrame({'close': [10, 12, 15, 15, 10]})
pct = calculate_price_change_pct(df, column='close')
print(pct)
```
