# src/data_loader.py

## Overview
Fetches historical stock data for a given ticker and period using yfinance. Returns a pandas DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].

## Function: fetch_data

Fetches historical stock data for a given ticker, period, and interval using yfinance.

**Signature:**
```python
def fetch_data(ticker: str, period: str = "max", interval: str = "1d", columns: List[str] = None, use_cache: bool = True) -> pd.DataFrame
```
- **ticker**: Stock ticker symbol (e.g., 'AAPL').
- **period**: Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.
- **interval**: Data interval (e.g., '1d', '1wk'). Defaults to '1d'.
- **columns**: List of columns to return. If None, returns standard columns.
- **use_cache**: Whether to use cached data if available. Defaults to True.

**Returns:**
- `pd.DataFrame`: DataFrame with requested columns (default: ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

**Raises:**
- `ValueError`: If input parameters are invalid or data is empty.

**Logging:**
- Logs key events, errors, and warnings for observability.

**Example Usage:**
```python
from src import data_loader

# Get all standard columns
df = data_loader.fetch_data('AAPL', period='1y')
print(df.head())

# Only get specific columns
df = data_loader.fetch_data('AAPL', period='1y', columns=['Open', 'Close'])
print(df.head())

# Bypass cache
df = data_loader.fetch_data('AAPL', period='1y', use_cache=False)
print(df.head())
```

## Function: fetch

Fetches historical stock data for a given ticker and period with additional options for column filtering and cache control.

**Signature:**
```python
def fetch(ticker: str, period: str = "1y", columns: List[str] = None, use_cache: bool = True) -> pd.DataFrame
```
- **ticker**: Stock ticker symbol (e.g., 'AAPL').
- **period**: Data period (e.g., '1y', '6mo', 'max'). Defaults to '1y'.
- **columns**: List of columns to return. If None, returns all columns.
- **use_cache**: Whether to use cached data if available. Defaults to True.

**Returns:**
- `pd.DataFrame`: DataFrame with requested columns.

**Raises:**
- `ValueError`: If input parameters are invalid or data is empty.

**Notes:**
- This function is a thin wrapper around `fetch_data` for backward compatibility.
- For new code, prefer using `fetch_data` directly.
- Always uses '1d' interval (daily data).

**Example Usage:**
```python
from src import data_loader

df = data_loader.fetch('AAPL', period='1y')
print(df.head())

# Only get specific columns
df = data_loader.fetch('AAPL', period='1y', columns=['Open', 'Close'])
print(df.head())

# Bypass cache
df = data_loader.fetch('AAPL', period='1y', use_cache=False)
print(df.head())
```

## Testing
- Unit tests in `tests/test_data_loader.py` use mocks for yfinance. All mocks and test DataFrames must include 'Adj Close' in the default columns.
- Comprehensive tests focus on the primary `fetch_data` function, including validation, column selection, cache control, and error handling.
- The `fetch` function is tested only with a single targeted test `test_fetch_delegates_to_fetch_data` that verifies it correctly delegates to the primary function.
- Integration tests (recommended) should verify real API behavior (optionally skipped by default).

## Notes
- This function replaces any previous start/end date interface with a period-based interface for simplicity and reliability.
- The `fetch` function is maintained as a backward-compatibility wrapper around `fetch_data`.
- For new code, prefer using `fetch_data` directly as it is the primary interface specified in the design.
