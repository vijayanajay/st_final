# Project Directory Structure

This document describes the directory structure for the Simple Stock Strategy Backtester (S3B) project. It is kept up-to-date with the codebase and should be referenced for any architectural or onboarding questions.

## Root Directories

- `src/` — Source code for all modules and business logic.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
- `configs/` — Configuration files for strategies, data sources, and environment settings.
    - `README.md` — Placeholder and documentation for configuration conventions.
- `tests/` — All pytest-based tests for business logic and modules.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
- `docs/` — Project documentation (including this file, codebase overview, PRD, and tasks).
- `requirements.txt` — Python dependency manifest listing all required third-party packages for the project. Must include only minimal, necessary dependencies as per PRD and codebase policy.

## File Descriptions

- **src/data_loader.py**: Provides `fetch(ticker, period="max")` to retrieve historical stock data using yfinance. Returns a DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume']. Period is a string like '1y', '6mo', or 'max' (default).

## Notes
- Each directory contains a placeholder file to ensure it is tracked in version control.
- All code and documentation changes must be reflected here and in docs/codebase_overview.md.
- If you add, remove, or rename directories, update this file immediately.
