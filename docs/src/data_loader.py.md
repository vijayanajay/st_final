# src/data_loader.py

## Overview
Fetches historical stock data for a given ticker and period using yfinance. Returns a pandas DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume'].

## Function: fetch

**Signature:**
```python
def fetch(ticker: str, period: str = "max") -> pd.DataFrame:
```

**Arguments:**
- `ticker` (str): Stock ticker symbol (e.g., 'AAPL').
- `period` (str, optional): Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.

**Returns:**
- `pd.DataFrame`: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume']

**Raises:**
- `ValueError`: If input parameters are invalid or data is empty.

**Logging:**
- Logs info, warnings, and errors for observability and debugging.

**Example Usage:**
```python
from src import data_loader

df = data_loader.fetch('AAPL', period='1y')
print(df.head())
```

## Testing
- Unit tests in `tests/test_data_loader.py` use mocks for yfinance.
- Integration tests (recommended) should verify real API behavior (optionally skipped by default).

## Notes
- This function replaces any previous start/end date interface with a period-based interface for simplicity and reliability.
