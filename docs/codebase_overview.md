# Codebase Overview

This document provides a high-level overview of the Simple Stock Strategy Backtester (S3B) codebase. It is intended for onboarding, architectural reference, and ensuring alignment between code and documentation.

## Directory Structure

See docs/file_structure.md for a detailed directory and file listing.

- **src/**: Contains all source code modules and business logic. Each module is documented with inline docstrings and, where appropriate, a corresponding markdown file in docs/.
- **configs/**: Contains configuration files (YAML, JSON, etc.) for strategies, data sources, and environment settings. See configs/README.md for details.
- **tests/**: Contains all pytest-based tests for business logic and modules. Each test module should correspond to a module in src/.
- **docs/**: Contains all project documentation, including this overview, file structure, PRD, and task tracking.
    - `src/`: Directory containing markdown documentation for corresponding `src/` modules.
- **requirements.txt**: Python dependency manifest at the project root. Lists all required third-party packages (pandas, numpy, yfinance, pyyaml) and must remain minimal as per project policy.

## Documentation Policy
- All code changes must be reflected in this file and docs/file_structure.md.
- If you add, remove, or rename modules, update this file and create or update docs/[filepath].md as needed.
- Discrepancies between code and documentation must be flagged and resolved immediately.

## Onboarding Checklist
- Review docs/file_structure.md for directory layout.
- Review this file for codebase context.
- Ensure all modules and tests are under 500 lines per file.
- Confirm all business logic is tested and documented.

## data_loader.py

**Location:** src/data_loader.py

**Purpose:**
Fetches historical stock data for a given ticker and period using yfinance. Returns a pandas DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].

**Key Function:**
- `fetch(ticker: str, period: str = "max", columns: Optional[List[str]] = None, use_cache: bool = True) -> pd.DataFrame`
    - **ticker**: Stock ticker symbol (e.g., 'AAPL').
    - **period**: Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.
    - **columns**: Optional list of columns to return. If None, all columns are returned.
    - **use_cache**: Whether to use cached data if available. Defaults to True.
    - **Returns**: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    - **Raises**: ValueError if input is invalid or data is empty.
    - **Logging**: Logs key events, errors, and warnings for observability.

**Example Usage:**
```python
from src import data_loader

df = data_loader.fetch('AAPL', period='1y')
print(df.head())
```

**Testing:**
- Unit tests in `tests/test_data_loader.py` use mocks for yfinance. All mocks and test DataFrames must include 'Adj Close' in the default columns.
- Integration tests (recommended) should verify real API behavior (optionally skipped by default).

## feature_generator.py

**Location:** src/feature_generator.py

**Purpose:**
Provides feature engineering utilities for stock trading strategies, currently including calculation of Simple Moving Averages (SMA), 1-day price change percentage, and volatility (calculate_volatility) with robust input validation and error handling. Logging is handled generically at the application level; this module emits structured log messages for all error conditions and critical operations.

**Key Functions:**
- `calculate_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series`
    - **df**: Input DataFrame containing price data.
    - **column**: Name of the column to calculate SMA on.
    - **window**: Window size for the moving average. Must be > 0.
    - **Returns**: Series containing the SMA values, named as 'sma_{window}'.
    - **Raises**: ValueError if the column does not exist or window is invalid.
    - **Logging**: Structured logging is implemented for all error conditions and critical operations using the standard library `logging` module. Logging configuration is centralized in `configs/logging_config.py`.
- `calculate_price_change_pct(df: pd.DataFrame, column: str = "close") -> pd.Series`
    - **df**: Input DataFrame containing price data.
    - **column**: Name of the column to calculate price change percentage on. Defaults to 'close'.
    - **Returns**: Series containing the 1-day price change percentage, named as 'price_change_pct_1d'.
    - **Raises**: ValueError if the column does not exist or is not numeric.
    - **Logging**: Structured logging is implemented for all error conditions and critical operations using the standard library `logging` module. Logging configuration is centralized in `configs/logging_config.py`.
- `calculate_volatility(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series`
    - **df**: Input DataFrame containing price data.
    - **column**: Name of the column to calculate volatility on. Defaults to 'close'.
    - **window**: Window size for the rolling standard deviation. Must be > 0.
    - **Returns**: Series containing the rolling volatility, named as 'volatility_{window}'.
    - **Raises**: ValueError if the column does not exist, is not numeric, or window is invalid.
    - **Logging**: Structured logging is implemented for all error conditions and critical operations using the standard library `logging` module. Logging configuration is centralized in `configs/logging_config.py`.

**Example Usage:**
```python
from src.feature_generator import calculate_sma, calculate_price_change_pct, calculate_volatility
 import pandas as pd

df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
sma = calculate_sma(df, column='close', window=3)
pct = calculate_price_change_pct(df, column='close')
vol = calculate_volatility(df, column='close', window=3)
print(sma)
print(pct)
print(vol)
```

**Testing:**
- Unit tests in `tests/test_feature_generator.py` cover correctness, edge cases, and compliance with the logging standard for all three functions.

## config_parser.py

**Location:** src/config_parser.py

**Purpose:**
Loads and validates YAML configuration files for trading strategies. Ensures all required fields are present and the configuration is properly formatted.

**Key Function:**
- `load_config(path: str) -> dict`
    - **path**: Path to the YAML config file.
    - **Returns**: Dict containing the parsed configuration.
    - **Raises**: FileNotFoundError if the file does not exist, ValueError if YAML is invalid or required fields are missing.
    - **Logging**: Logs errors for missing files, invalid YAML, and missing required fields. All log messages use standard error types for testability and observability.

**Example Usage:**
```python
from src import config_parser

try:
    config = config_parser.load_config('configs/strategies/sma_cross.yaml')
    print(config)
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
```

**Testing:**
- Unit tests in `tests/test_config_parser.py` cover loading valid configs, handling missing files, handling invalid YAML, and handling missing required fields.
- Tests verify both function behavior and appropriate logging of events using pytest's `caplog` fixture.

## strategies.py

**Location:** src/strategies.py

**Purpose:**
This module contains the logic for different trading strategies. It defines a BaseStrategy class and implements the generate_sma_crossover_signals function for SMA crossover strategies.

**Key Classes:**
- `BaseStrategy`
    - **Purpose:** Serves as a foundational class for all strategy implementations.
    - **Attributes:** (To be defined)
    - **Methods:** (To be defined)

**Example Usage:**
```python
from src.strategies import BaseStrategy

# Further implementation will involve creating subclasses of BaseStrategy
# class MyStrategy(BaseStrategy):
#     def __init__(self, params):
#         super().__init__()
#         self.params = params
#
#     def generate_signals(self, data):
#         # Strategy logic to generate buy/sell signals
#         pass
```

**Testing:**
- Unit tests in `tests/test_strategies.py` will verify the functionality of the `BaseStrategy` class and any implemented strategies.
- Initial tests ensure the module can be imported and the `BaseStrategy` class exists.
