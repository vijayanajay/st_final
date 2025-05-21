# Project Directory Structure

This document describes the directory structure for the Simple Stock Strategy Backtester (S3B) project. It is kept up-to-date with the codebase and should be referenced for any architectural or onboarding questions.

## Root Directories

- `src/` — Source code for all modules and business logic.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
    - `data_loader.py` — Provides modular, validated, and parameterized access to historical stock data using yfinance. Supports column selection (default: ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']), input validation, optional in-memory caching, and structured logging (logging config is not set here; see configs/logging_config.py). All test mocks must include 'Adj Close' in the default columns.
    - `feature_generator.py` — Provides feature engineering utilities for stock trading strategies. The primary interface consists of add_sma, add_price_change_pct_1d, add_volatility_nday, and the generate_features orchestrator, all of which add features directly to DataFrames with robust input validation, error handling, and structured logging. The calculate_* functions (e.g., calculate_volatility) are backward-compatibility aliases and not the main API. See docs/src/feature_generator.py.md for full API and usage details. Regularly audit this description against the module and design.md to ensure accuracy.
    - `config_parser.py` — Utility for loading and validating YAML configuration files.
    - `strategies.py` — Module for implementing trading strategies, including a BaseStrategy class and the generate_sma_crossover_signals function.
- `configs/` — Configuration files for strategies, data sources, environment settings, and logging.
    - `logging_config.py` — Centralized logging configuration. Should be imported and called from the main application entry point.
    - `README.md` — Placeholder and documentation for configuration conventions.
- `tests/` — All pytest-based tests for business logic and modules.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
    - `test_data_loader.py` — Tests for src/data_loader.py, including both unit (mocked) and integration (real API, optionally skipped) tests.
    - `test_feature_generator.py` — Tests for src/feature_generator.py.
    - `test_config_parser.py` — Tests for src/config_parser.py.
    - `test_strategies.py` — Tests for src/strategies.py.
- `docs/` — Project documentation (including this file, codebase overview, PRD, and tasks).
    - `codebase_overview.md` — High-level overview of the codebase and documentation policy.
    - `file_structure.md` — This file. Describes the directory and file structure.
    - `prd.md`, `tasks.md` — Product requirements and task tracking.
    - `src/` — All module-specific documentation markdown files are located here. The convention is strictly: `docs/src/<module_name>.py.md`.
        - `config_parser.py.md` — Documentation for src/config_parser.py.
        - `data_loader.py.md` — Documentation for src/data_loader.py.
        - `feature_generator.py.md` — Documentation for src/feature_generator.py.
        - `strategies.py.md` — Documentation for src/strategies.py.

## File Descriptions

- **src/data_loader.py**: Provides modular, validated, and parameterized access to historical stock data using yfinance. Supports column selection (default: ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']), input validation, optional in-memory caching, and structured logging (logging config is not set here; see configs/logging_config.py).
- **src/feature_generator.py**: Provides feature engineering utilities for stock trading strategies. The primary interface consists of add_sma, add_price_change_pct_1d, add_volatility_nday, and the generate_features orchestrator, all of which add features directly to DataFrames with robust input validation, error handling, and structured logging. The calculate_* functions (e.g., calculate_volatility) are backward-compatibility aliases and not the main API. See docs/src/feature_generator.py.md for full API and usage details. Regularly audit this description against the module and design.md to ensure accuracy.
- **src/config_parser.py**: Utility for loading and validating YAML configuration files. See docs/src/config_parser.py.md for API and usage details.
- **src/strategies.py**: Module for implementing trading strategies. Includes a `BaseStrategy` class and the `generate_sma_crossover_signals` function. See docs/src/strategies.py.md for API and usage details.

## Notes
- Each directory contains a placeholder file to ensure it is tracked in version control.
- All code and documentation changes must be reflected here, in docs/codebase_overview.md, and in the relevant docs/src/[module_name].py.md files.
- If you add, remove, or rename directories or files, update this file and related documentation immediately.
- **Documentation Path Convention:** All module-specific documentation markdown files must be located in `docs/src/` and named `<module_name>.py.md`. Any other path is incorrect and must be corrected immediately. This convention is enforced for clarity and consistency.
