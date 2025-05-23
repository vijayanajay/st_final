# src/feature_generator.py.md

# Feature Generator Module Documentation

## Overview
This module provides feature engineering utilities for stock trading, including calculation of Simple Moving Averages (SMA).

## Functions

### add_sma

**Signature:**
```python
def add_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
```

**Description:**
Adds Simple Moving Average (SMA) to the DataFrame.

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
- A backward-compatibility alias `calculate_sma` is provided that delegates to this function.

**Testing:**
- All functions are tested in `tests/test_feature_generator.py` for correctness, edge cases, and error handling.
- Tests use static, pre-calculated expected values rather than dynamic recalculation to ensure independent verification of function correctness.
- Logging of error conditions is explicitly tested using pytest's `caplog` fixture to ensure observability and compliance with project requirements.

**Example:**
```python
import pandas as pd
from src.feature_generator import add_sma

df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
sma = add_sma(df, column='close', window=3)
print(sma)
```

---

### calculate_sma

**Signature:**
```python
def calculate_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
```

**Description:**
This is an alias for `add_sma` provided for backward compatibility with tests.

See `add_sma` for full documentation.

---

### add_price_change_pct_1d

**Signature:**
```python
def add_price_change_pct_1d(df: pd.DataFrame, column: str = "close") -> pd.Series:
```

**Description:**
Adds 1-day price change percentage to the DataFrame. The result is `(current - previous) / previous * 100` for each row.

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
- A backward-compatibility alias `calculate_price_change_pct` is provided that delegates to this function.

**Testing:**
- All functions are tested in `tests/test_feature_generator.py` for correctness, edge cases, and error handling.
- Tests use static, pre-calculated expected values rather than dynamic recalculation to ensure independent verification of function correctness.
- Logging of error conditions is explicitly tested using pytest's `caplog` fixture to ensure observability and compliance with project requirements.

**Example:**
```python
import pandas as pd
from src.feature_generator import add_price_change_pct_1d

df = pd.DataFrame({'close': [10, 12, 15, 15, 10]})
pct = add_price_change_pct_1d(df, column='close')
print(pct)
```

---

### calculate_price_change_pct

**Signature:**
```python
def calculate_price_change_pct(df: pd.DataFrame, column: str = "close") -> pd.Series:
```

**Description:**
This is an alias for `add_price_change_pct_1d` provided for backward compatibility with tests.

See `add_price_change_pct_1d` for full documentation.

---

### add_volatility_nday

**Signature:**
```python
def add_volatility_nday(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series:
```

**Description:**
Adds n-day rolling volatility to the DataFrame. The result is the rolling std of `(current - previous) / previous * 100` over the given window.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame containing price data.
- `column` (str, optional): Name of the column to calculate volatility on. Defaults to 'close'.
- `window` (int, optional): Window size for the rolling standard deviation. Must be > 0. Defaults to 20.

**Returns:**
- `pd.Series`: Series containing the rolling volatility, named as 'volatility_{window}'.

**Raises:**
- `ValueError`: If the column does not exist, is not numeric, or window is invalid.

**Notes:**
- Input validation and error handling are performed, with structured logging for all error conditions and critical operations (see code for logging details).
- Logging is handled using the standard library `logging` module, with configuration centralized in `configs/logging_config.py`.
- The function is tested in `tests/test_feature_generator.py`.
- A backward-compatibility alias `calculate_volatility` is provided that delegates to this function.

**Testing:**
- All functions are tested in `tests/test_feature_generator.py` for correctness, edge cases, and error handling.
- Tests use static, pre-calculated expected values rather than dynamic recalculation to ensure independent verification of function correctness.
- Logging of error conditions is explicitly tested using pytest's `caplog` fixture to ensure observability and compliance with project requirements.

**Example:**
```python
import pandas as pd
from src.feature_generator import add_volatility_nday

df = pd.DataFrame({'close': [10, 12, 15, 15, 10]})
vol = add_volatility_nday(df, column='close', window=3)
print(vol)
```

---

### calculate_volatility

**Signature:**
```python
def calculate_volatility(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series:
```

**Description:**
This is an alias for `add_volatility_nday` provided for backward compatibility with tests.

See `add_volatility_nday` for full documentation.

---

### generate_features

**Signature:**
```python
def generate_features(df: pd.DataFrame, feature_config: dict) -> pd.DataFrame:
```

**Description:**
Orchestrates feature generation as specified in feature_config.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame containing price data.
- `feature_config` (dict): Configuration dictionary specifying features to generate.

**Returns:**
- `pd.DataFrame`: DataFrame with added feature columns as specified in feature_config.

**Raises:**
- `ValueError`: If any specified feature in feature_config is invalid.

**Notes:**
- The function validates the feature_config against the available feature generation functions and their parameters.
- Logging is handled using the standard library `logging` module, with configuration centralized in `configs/logging_config.py`.
- The function is tested in `tests/test_feature_generator.py`.

**Testing:**
- All functions are tested in `tests/test_feature_generator.py` for correctness, edge cases, and error handling.
- Logging of error conditions is explicitly tested using pytest's `caplog` fixture to ensure observability and compliance with project requirements.

**Example:**
```python
import pandas as pd
from src.feature_generator import generate_features

df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
feature_config = {'sma': {'column': 'close', 'window': 3}}
features_df = generate_features(df, feature_config)
print(features_df)
```
