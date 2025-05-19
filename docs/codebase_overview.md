# Codebase Overview

This document provides a high-level overview of the Simple Stock Strategy Backtester (S3B) codebase. It is intended for onboarding, architectural reference, and ensuring alignment between code and documentation.

## Directory Structure

See docs/file_structure.md for a detailed directory and file listing.

- **src/**: Contains all source code modules and business logic. Each module is documented with inline docstrings and, where appropriate, a corresponding markdown file in docs/.
- **configs/**: Contains configuration files (YAML, JSON, etc.) for strategies, data sources, and environment settings. See configs/README.md for details.
- **tests/**: Contains all pytest-based tests for business logic and modules. Each test module should correspond to a module in src/.
- **docs/**: Contains all project documentation, including this overview, file structure, PRD, and task tracking.
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
Fetches historical stock data for a given ticker and period using yfinance. Returns a pandas DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume'].

**Key Function:**
- `fetch(ticker: str, period: str = "max") -> pd.DataFrame`
    - **ticker**: Stock ticker symbol (e.g., 'AAPL').
    - **period**: Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.
    - **Returns**: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume']
    - **Raises**: ValueError if input is invalid or data is empty.
    - **Logging**: Logs key events, errors, and warnings for observability.

**Example Usage:**
```python
from src import data_loader

df = data_loader.fetch('AAPL', period='1y')
print(df.head())
```

**Testing:**
- Unit tests in `tests/test_data_loader.py` use mocks for yfinance.
- Integration tests (recommended) should verify real API behavior (optionally skipped by default).

## feature_generator.py

**Location:** src/feature_generator.py

**Purpose:**
Provides feature engineering utilities for stock trading strategies, currently including calculation of Simple Moving Averages (SMA) with robust input validation and error handling. Logging is handled generically at the application level; this module does not emit log messages directly.

**Key Function:**
- `calculate_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series`
    - **df**: Input DataFrame containing price data.
    - **column**: Name of the column to calculate SMA on.
    - **window**: Window size for the moving average. Must be > 0.
    - **Returns**: Series containing the SMA values, named as 'sma_{window}'.
    - **Raises**: ValueError if the column does not exist or window is invalid.
    - **Logging**: Structured logging is now implemented for all error conditions and critical operations using the standard library `logging` module. Logging configuration is centralized in `configs/logging_config.py`.

**Example Usage:**
```python
from src.feature_generator import calculate_sma
import pandas as pd

df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
sma = calculate_sma(df, column='close', window=3)
print(sma)
```

**Testing:**
- Unit tests in `tests/test_feature_generator.py` cover correctness, edge cases, and compliance with the logging standard.

---
