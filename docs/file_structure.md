# Project Directory Structure

This document describes the directory structure for the Simple Stock Strategy Backtester (S3B) project. It is kept up-to-date with the codebase and should be referenced for any architectural or onboarding questions.

## Root Directories

- `src/` — Source code for all modules and business logic.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
    - `data_loader.py` — Provides modular, validated, and parameterized access to historical stock data using yfinance. Supports column selection, input validation, optional in-memory caching, and structured logging (logging config is not set here; see configs/logging_config.py).
    - `feature_generator.py` — Provides feature engineering utilities, including calculation of Simple Moving Averages (SMA) and 1-day price change percentage (see `calculate_price_change_pct`). Both functions include input validation, error handling, and structured logging. See docs/src/feature_generator.py.md for API and usage details.
- `configs/` — Configuration files for strategies, data sources, environment settings, and logging.
    - `logging_config.py` — Centralized logging configuration. Should be imported and called from the main application entry point.
    - `README.md` — Placeholder and documentation for configuration conventions.
- `tests/` — All pytest-based tests for business logic and modules.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
    - `test_data_loader.py` — Tests for src/data_loader.py, including both unit (mocked) and integration (real API, optionally skipped) tests.
- `docs/` — Project documentation (including this file, codebase overview, PRD, and tasks).
    - `data_loader.py.md` — Documentation for src/data_loader.py, including API, usage, and design notes.
    - `codebase_overview.md` — High-level overview of the codebase and documentation policy.
    - `file_structure.md` — This file. Describes the directory and file structure.
    - `prd.md`, `tasks.md` — Product requirements and task tracking.
- `requirements.txt` — Python dependency manifest listing all required third-party packages for the project. Must include only minimal, necessary dependencies as per PRD and codebase policy.

## File Descriptions

- **src/data_loader.py**: Provides modular, validated, and parameterized access to historical stock data using yfinance. Supports column selection, input validation, optional in-memory caching, and structured logging (logging config is not set here; see configs/logging_config.py).
- **src/feature_generator.py**: Provides feature engineering utilities, including calculation of Simple Moving Averages (SMA) and 1-day price change percentage (see `calculate_price_change_pct`). Both functions include input validation, error handling, and structured logging. See docs/src/feature_generator.py.md for API and usage details.

## Notes
- Each directory contains a placeholder file to ensure it is tracked in version control.
- All code and documentation changes must be reflected here, in docs/codebase_overview.md, and in the relevant docs/[filepath].md files (e.g., docs/data_loader.py.md, configs/logging_config.py.md).
- If you add, remove, or rename directories or files, update this file and related documentation immediately.
