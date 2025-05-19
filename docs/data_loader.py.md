# src/data_loader.py

## Overview
Fetches historical stock data for a given ticker and period using yfinance. Returns a pandas DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume'] or a user-specified subset. Supports input validation, parameterized column selection, and optional in-memory caching for performance.

## Function: fetch

**Signature:**
```python
def fetch(
    ticker: str,
    period: str = "max",
    columns: Optional[List[str]] = None,
    use_cache: bool = True
) -> pd.DataFrame:
```

**Arguments:**
- `ticker` (str): Stock ticker symbol (e.g., 'AAPL').
- `period` (str, optional): Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.
- `columns` (List[str], optional): Columns to return. Defaults to ['Open', 'High', 'Low', 'Close', 'Volume'].
- `use_cache` (bool, optional): Use in-memory cache for repeated queries. Defaults to True.

**Returns:**
- `pd.DataFrame`: DataFrame with requested columns.

**Raises:**
- `ValueError`: If input parameters are invalid or data is empty.

**Logging:**
- Uses the standard logging module for observability. Logging configuration is not set in this module; it should be configured once in the main application using `configs/logging_config.py`.

**Example Usage:**
```python
from src import data_loader
from configs.logging_config import setup_logging

setup_logging()
df = data_loader.fetch('AAPL', period='1y', columns=['Open', 'Close'])
```

## Helper Functions
- `validate_ticker`, `validate_period`, `validate_columns`: Input and output validation. Raise ValueError on invalid input or missing columns.
- `_fetch_data`, `_cached_fetch_data`: Internal functions for data retrieval. `_cached_fetch_data` uses functools.lru_cache for in-memory caching.

## Testing
- Unit tests in `tests/test_data_loader.py` use mocks for yfinance.
- Integration tests (recommended) should verify real API behavior (optionally skipped by default).

## Notes
- All input validation and error handling is modularized for testability.
- Caching is optional and can be disabled per call.
- For logging to work, ensure the main application configures logging as described above.
