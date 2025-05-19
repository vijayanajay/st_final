# src/data_loader.py

## Overview
This module provides functions to fetch historical stock data using yfinance, with a focus on correctness, modularity, and observability. It supports input validation, parameterized column selection, and optional in-memory caching for performance.

## Key Functions

### fetch
Fetches historical stock data for a given ticker and period.
- **Parameters:**
    - `ticker` (str): Stock ticker symbol (e.g., 'AAPL').
    - `period` (str, optional): Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.
    - `columns` (List[str], optional): Columns to return. Defaults to ['Open', 'High', 'Low', 'Close', 'Volume'].
    - `use_cache` (bool, optional): Use in-memory cache for repeated queries. Defaults to True.
- **Returns:**
    - `pd.DataFrame` with requested columns.
- **Raises:**
    - `ValueError` if input parameters are invalid or data is empty.

### validate_ticker, validate_period, validate_columns
Helper functions for input and output validation. Raise ValueError on invalid input or missing columns.

### _fetch_data, _cached_fetch_data
Internal functions for data retrieval. `_cached_fetch_data` uses functools.lru_cache for in-memory caching.

## Logging
- Uses the standard logging module for observability.
- Logging configuration is not set in this module. It should be configured once in the main application using `configs/logging_config.py`.

## Example Usage
```python
from src import data_loader
from configs.logging_config import setup_logging

setup_logging()
df = data_loader.fetch('AAPL', period='1y', columns=['Open', 'Close'])
```

## Notes
- All input validation and error handling is modularized for testability.
- Caching is optional and can be disabled per call.
- For logging to work, ensure the main application configures logging as described above.
