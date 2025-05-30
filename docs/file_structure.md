# Project Directory Structure

This document describes the directory structure for the Simple Stock Strategy Backtester (S3B) project. It is kept up-to-date with the codebase and should be referenced for any architectural or onboarding questions.

## Root Directories

- `src/` — Source code for all modules and business logic.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
    - `data_loader.py` — Provides modular, validated, and parameterized access to historical stock data using yfinance. Primary interface is fetch_data which supports column selection, interval parameters, period configuration, cache control, and comprehensive input validation. The fetch function is maintained as a backward-compatibility wrapper around fetch_data. Features structured logging (logging config is not set here; see configs/logging_config.py).
    - `feature_generator.py` — Provides feature engineering utilities for stock trading strategies. The primary interface consists of add_sma, add_price_change_pct_1d, add_volatility_nday, and the generate_features orchestrator, all of which add features directly to DataFrames with robust input validation, error handling, and structured logging. The calculate_* functions (e.g., calculate_volatility) are backward-compatibility aliases and not the main API. See docs/src/feature_generator.py.md for full API and usage details. Regularly audit this description against the module and design.md to ensure accuracy.    - `config_parser.py` — Utility for loading and validating YAML configuration files.
    - `strategies.py` — Module for implementing trading strategies using the Strategy Pattern. Includes an abstract `BaseStrategy` class, concrete strategy implementations like `SMACrossoverStrategy`, and utility functions for applying strategies. 
    - `backtester.py` — Provides the complete simulation framework for backtesting trading strategies based on generated signals. Implements both basic and enhanced backtesting capabilities with comprehensive portfolio tracking, position management, and analytics. The primary interfaces are `run_backtest` (basic mode) and `run_backtest_enhanced` (detailed analytics mode), supporting trade execution simulation, portfolio composition tracking, returns calculation, and drawdown analysis. Features the PortfolioData structure for enhanced analytics and maintains backward compatibility. See docs/src/backtester.py.md for full API and usage details.
    - `metrics.py` — Performance metrics calculation module for analyzing backtesting results. Provides total return and annualized return calculations from trade logs and portfolio value series. Primary interfaces are `calculate_metrics` (for computing performance metrics) and `print_metrics` (for formatted console output). Features comprehensive input validation, intelligent time-series handling for annualization, and extensible architecture for future metrics. See docs/src/metrics.py.md for full API and usage details.
- `configs/` — Configuration files for strategies, data sources, environment settings, and logging.
    - `logging_config.py` — Centralized logging configuration. Should be imported and called from the main application entry point.
    - `README.md` — Placeholder and documentation for configuration conventions.
- `tests/` — All pytest-based tests for business logic and modules.
    - `__init__.py` — Ensures the directory is recognized as a Python package.    - `test_data_loader.py` — Tests for src/data_loader.py, including both unit (mocked) and integration (real API, optionally skipped) tests.
    - `test_feature_generator.py` — Tests for src/feature_generator.py.
    - `test_config_parser.py` — Tests for src/config_parser.py.    - `test_strategies.py` — Tests for the `generate_sma_crossover_signals` function in src/strategies.py.
    - `test_apply_strategy.py` — Comprehensive tests for the apply_strategy function in src/strategies.py, covering correct signal generation, parameter validation, different column names, empty DataFrames, NaN handling, logging verification, and DataFrame immutability.
    - `test_strategy_pattern.py` — Tests for the Strategy pattern implementation in src/strategies.py, including tests for `BaseStrategy`, `SMACrossoverStrategy`, and the strategy registry.
    - `test_integration.py` — Integration tests that verify multiple modules work together correctly, using the recommended primary API (`apply_strategy`). Includes feature generation and strategy integration tests, legacy feature config compatibility tests, multi-feature type tests, and an end-to-end test that generates result files. This properly integrated pytest test replaces the standalone integration_test.py that previously existed in the project root.
    - `test_backtester.py` — Comprehensive tests for src/backtester.py, covering both basic and enhanced backtesting functionality with 22 tests for position tracking, trade execution, portfolio valuation, and analytics.
    - `test_metrics.py` — Tests for src/metrics.py, including 16 comprehensive tests covering basic return calculations, edge cases, error handling, and console output formatting.
- `docs/` — Project documentation (including this file, codebase overview, PRD, and tasks).
    - `codebase_overview.md` — High-level overview of the codebase and documentation policy.
    - `file_structure.md` — This file. Describes the directory and file structure.
    - `prd.md`, `tasks.md` — Product requirements and task tracking.    - `src/` — All module-specific documentation markdown files are located here. The convention is strictly: `docs/src/<module_name>.py.md`.
        - `config_parser.py.md` — Documentation for src/config_parser.py.
        - `data_loader.py.md` — Documentation for src/data_loader.py.
        - `feature_generator.py.md` — Documentation for src/feature_generator.py.
        - `strategies.py.md` — Documentation for src/strategies.py.
        - `backtester.py.md` — Documentation for src/backtester.py.
        - `metrics.py.md` — Documentation for src/metrics.py.
    - `tests/` — Documentation for test files.
        - `test_data_loader.py.md` — Documentation for tests/test_data_loader.py.
        - `test_feature_generator.py.md` — Documentation for tests/test_feature_generator.py.
        - `test_integration.py.md` — Documentation for tests/test_integration.py.
        - `test_config_parser.py.md` — Documentation for tests/test_config_parser.py.
        - `test_strategies.py.md` — Documentation for tests/test_strategies.py.
        - `test_apply_strategy.py.md` — Documentation for tests/test_apply_strategy.py.
        - `test_strategy_pattern.py.md` — Documentation for tests/test_strategy_pattern.py.
        - `test_backtester.py.md` — Documentation for tests/test_backtester.py.
        - `test_metrics.py.md` — Documentation for tests/test_metrics.py.

## File Descriptions

- **src/data_loader.py**: Provides modular, validated, and parameterized access to historical stock data using yfinance. Primary interface `fetch_data` supports column selection, interval parameters, period configuration, cache control, and comprehensive input validation. The `fetch` function is maintained as a backward-compatibility wrapper. See docs/src/data_loader.py.md for complete API details.
- **src/feature_generator.py**: Provides feature engineering utilities for stock trading strategies. The primary interface consists of add_sma, add_price_change_pct_1d, add_volatility_nday, and the generate_features orchestrator, all of which add features directly to DataFrames with robust input validation, error handling, and structured logging. The calculate_* functions (e.g., calculate_volatility) are backward-compatibility aliases and not the main API. See docs/src/feature_generator.py.md for full API and usage details. Regularly audit this description against the module and design.md to ensure accuracy.
- **src/config_parser.py**: Utility for loading and validating YAML configuration files. See docs/src/config_parser.py.md for API and usage details.
- **src/strategies.py**: Module for implementing trading strategies using the Strategy Pattern. Includes an abstract `BaseStrategy` class with an interface for strategy implementations, concrete strategy classes like `SMACrossoverStrategy`, a strategy registry for dynamic instantiation, and utility functions like `generate_sma_crossover_signals` (kept for backward compatibility) and `apply_strategy` for applying different strategies to data. See docs/src/strategies.py.md for API and usage details.
- **src/backtester.py**: Provides the complete simulation framework for backtesting trading strategies based on generated signals. Implements both basic (`run_backtest`) and enhanced (`run_backtest_enhanced`) backtesting capabilities with comprehensive portfolio tracking, position management, and analytics. Features include trade execution simulation, portfolio composition tracking (cash vs equity breakdown with exactly 0% cash/100% equity when in position), period and cumulative returns calculation, drawdown analysis, and the PortfolioData NamedTuple structure for enhanced analytics. Maintains full backward compatibility while offering detailed portfolio insights. See docs/src/backtester.py.md for complete API and usage details.
- **src/metrics.py**: Performance metrics calculation module for analyzing backtesting results. Provides total return and annualized return calculations from trade logs and portfolio value series. Primary interfaces are `calculate_metrics` (for computing performance metrics with intelligent time-series handling) and `print_metrics` (for formatted console output). Features comprehensive input validation, intelligent time-series handling for annualization, extensible architecture for future metrics, and proper handling of edge cases like zero-duration periods. See docs/src/metrics.py.md for complete API and usage details.

## Notes
- Each directory contains a placeholder file to ensure it is tracked in version control.
- All code and documentation changes must be reflected here, in docs/codebase_overview.md, and in the relevant docs/src/[module_name].py.md files.
- If you add, remove, or rename directories or files, update this file and related documentation immediately.
- **Documentation Path Convention:** All module-specific documentation markdown files must be located in `docs/src/` and named `<module_name>.py.md`. Any other path is incorrect and must be corrected immediately. This convention is enforced for clarity and consistency.
