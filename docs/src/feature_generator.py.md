# src/feature_generator.py.md

# Feature Generator Module Documentation

## Overview
This module provides feature engineering utilities for stock trading, including calculation of Simple Moving Averages (SMA).

### API Design
The module follows a clear API design pattern:
- Primary API Functions: The `add_*` functions (e.g., `add_sma`, `add_price_change_pct_1d`, `add_volatility_nday`) are the primary interface for this module.
- Legacy Aliases: The `calculate_*` functions are provided only for backward compatibility and delegate to their respective primary API functions.

### Testing Philosophy
- All tests directly target the primary API functions (`add_*`) with complete test coverage.
- Legacy aliases (`calculate_*`) have minimal tests to verify they correctly delegate to their primary counterparts.
- This ensures the documented public interface is thoroughly tested while maintaining backward compatibility.

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
- `ValueError`: If the column does not exist, is not numeric, or window is invalid.

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
Orchestrates feature generation as specified in feature_config. This function supports multiple configurations for the same feature type (e.g., multiple SMAs with different window sizes).

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame containing price data.
- `feature_config` (dict): Configuration dictionary specifying features to generate. The configuration can be structured in three ways:

  1. Named feature instances with a 'type' field:
     ```python
     {
         "SMA_short": {"type": "sma", "column": "close", "window": 20},
         "SMA_long": {"type": "sma", "column": "close", "window": 50},
         "Custom_Volatility": {"type": "volatility_nday", "column": "close", "window": 30}
     }
     ```

  2. Predefined list keys for multiple configurations of the same feature type:
     ```python
     {
         "smas": [
             {"name": "SMA_short", "column": "close", "window": 20},
             {"name": "SMA_long", "column": "close", "window": 50}
         ],
         "volatility_metrics": [
             {"name": "volatility_20", "column": "close", "window": 20}
         ]
     }
     ```
     Valid list keys are: `"smas"`, `"price_changes"`, `"volatility_metrics"`

  3. Legacy format (for backward compatibility):
     ```python
     {
         "sma": {"column": "close", "window": 20},
         "price_change_pct_1d": {"column": "close"},
         "volatility_nday": {"column": "close", "window": 20}
     }
     ```

**Returns:**
- `pd.DataFrame`: DataFrame with added feature columns as specified in feature_config.

**Raises:**
- `ValueError`: If any specified feature in feature_config is invalid.

**Notes:**
- The function supports multiple instances of the same feature type (e.g., multiple SMAs with different window sizes).
- For the list-based configuration (format 2), each item must include a 'name' field to specify the output column name.
- For the named instance configuration (format 1), the key is used as the output column name.
- For the legacy format (format 3), the output column name is determined by the underlying feature function.
- The function recognizes specific list keys (`"smas"`, `"price_changes"`, `"volatility_metrics"`) for list-based configurations.
- List keys not in the predefined set will be ignored with a warning.
- **Column name conflict resolution**: If a generated feature's column name already exists in the DataFrame, the function will automatically rename the new column by appending a numerical suffix (e.g., `sma_3_1`, `sma_3_2`) to avoid overwriting existing data. This ensures that no data is lost during feature generation and multiple instances of similar features can coexist.
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

# Format 1: Named instances with type
feature_config = {
    "SMA_short": {"type": "sma", "column": "close", "window": 20},
    "SMA_long": {"type": "sma", "column": "close", "window": 50}
}
features_df = generate_features(df, feature_config)
print(features_df)

# Format 2: Using predefined list keys
feature_config = {
    "smas": [
        {"name": "SMA_short", "column": "close", "window": 20},
        {"name": "SMA_long", "column": "close", "window": 50}
    ]
}
features_df = generate_features(df, feature_config)
print(features_df)

# Format 3: Legacy format
feature_config = {'sma': {'column': 'close', 'window': 20}}
features_df = generate_features(df, feature_config)
print(features_df)
```

---

### _add_feature (Helper Function)

**Signature:**
```python
def _add_feature(df: pd.DataFrame, feature_type: str, params: dict, output_name: str = None) -> pd.DataFrame:
```

**Description:**
Helper function to add a specific feature to the DataFrame. This is an internal function used by `generate_features`.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame.
- `feature_type` (str): Type of feature to add ('sma', 'price_change_pct_1d', etc.).
- `params` (dict): Parameters for the feature calculation.
- `output_name` (str, optional): Custom name for the output column. If not provided, the default naming from the underlying function is used.

**Returns:**
- `pd.DataFrame`: DataFrame with the new feature added.

**Notes:**
- This function handles the actual generation of each feature and the column name conflict resolution.
- If `output_name` is provided, it will be used as the column name for the feature.
- If the generated column name already exists in the DataFrame, a numerical suffix will be appended to create a unique name.
- The function logs warnings when column conflicts occur and informs about the new column name.
- This function is internal and not meant to be called directly by users.
