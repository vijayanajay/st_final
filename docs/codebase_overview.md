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

**Key Functions:**
- `fetch_data(ticker: str, period: str = "max", interval: str = "1d", columns: List[str] = None, use_cache: bool = True) -> pd.DataFrame`
    - **Primary interface as specified in design.md.**
    - Fetches historical stock data for a given ticker, period, and interval using yfinance.
    - Supports column selection and cache control.
    - **Returns:** DataFrame with requested columns (default: ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    - **Raises:** ValueError if input is invalid or data is empty.
    - **Logging:** Logs key events, errors, and warnings for observability.
- `fetch(ticker: str, period: str = "1y", columns: Optional[List[str]] = None, use_cache: bool = True) -> pd.DataFrame`
    - Backward-compatibility wrapper around `fetch_data`.
    - **Returns:** DataFrame with requested columns.
    - **Raises:** ValueError if input is invalid or data is empty.

**Example Usage:**
```python
from src import data_loader

df1 = data_loader.fetch_data('AAPL', period='1y', interval='1d')
df2 = data_loader.fetch_data('AAPL', period='1y', columns=['Open', 'Close'])
print(df1.head())
print(df2.head())
```

**Testing:**
- Unit tests in `tests/test_data_loader.py` use mocks for yfinance. All mocks and test DataFrames must include 'Adj Close' in the default columns.
- Integration tests (recommended) should verify real API behavior (optionally skipped by default).

**Documentation Policy Note:**
- All key public functions must be listed in this section. Cross-reference with design.md and docs/src/data_loader.py.md during documentation reviews to ensure completeness.

## feature_generator.py

**Location:** src/feature_generator.py

**Purpose:**
Provides feature engineering utilities for stock trading strategies. The module's primary interface consists of functions to add features directly to DataFrames, with robust input validation and error handling. Logging is handled generically at the application level; this module emits structured log messages for all error conditions and critical operations.

**Primary Interface Functions:**
- `add_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series`
    - Adds a Simple Moving Average (SMA) column to the DataFrame for the specified column and window.
    - Validates that the column is numeric, raising a ValueError with a clear message if not.
- `add_price_change_pct_1d(df: pd.DataFrame, column: str = "close") -> pd.Series`
    - Adds a 1-day price change percentage column to the DataFrame.
- `add_volatility_nday(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series`
    - Adds an n-day rolling volatility column to the DataFrame.
- `generate_features(df: pd.DataFrame, feature_config: dict) -> pd.DataFrame`
    - Orchestrates feature generation as specified in the feature_config dictionary.

**Backward-Compatibility Aliases:**
- `calculate_sma`, `calculate_price_change_pct`, and `calculate_volatility` are provided as aliases for legacy/test compatibility. They delegate to the corresponding add_* functions and should not be used as the primary API.

**Example Usage:**
```python
from src.feature_generator import add_sma, add_price_change_pct_1d, add_volatility_nday, generate_features
import pandas as pd

df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})

# Individual feature functions
sma = add_sma(df, column='close', window=3)
pct = add_price_change_pct_1d(df, column='close')
vol = add_volatility_nday(df, column='close', window=3)

# generate_features supports multiple configuration formats:

# 1. Named feature instances with "type" field (enables multiple features of same type)
config_named = {
    "SMA_short": {"type": "sma", "column": "close", "window": 5},
    "SMA_long": {"type": "sma", "column": "close", "window": 20},
    "Custom_Vol": {"type": "volatility_nday", "column": "close", "window": 10}
}
features_df1 = generate_features(df, config_named)

# 2. List-based configurations (predefined keys: "smas", "price_changes", "volatility_metrics")
config_lists = {
    "smas": [
        {"name": "SMA_10", "column": "close", "window": 10},
        {"name": "SMA_30", "column": "close", "window": 30}
    ],
    "volatility_metrics": [
        {"name": "Vol_5", "column": "close", "window": 5}
    ]
}
features_df2 = generate_features(df, config_lists)

# 3. Legacy format (backward compatibility)
config_legacy = {'sma': {'column': 'close', 'window': 3}}
features_df3 = generate_features(df, config_legacy)

print(sma)
print(pct)
print(vol)
print(features_df1.columns.tolist())  # ['close', 'SMA_short', 'SMA_long', 'Custom_Vol']
print(features_df2.columns.tolist())  # ['close', 'SMA_10', 'SMA_30', 'Vol_5']
print(features_df3.columns.tolist())  # ['close', 'sma_3']
```

**Testing:**
- Unit tests in `tests/test_feature_generator.py` cover correctness, edge cases, and compliance with the logging standard for all primary interface functions and aliases. As of 2025-05-23, redundant log assertion tests have been consolidated: all log message checks for error and info conditions are now performed in the main test_X_logging functions for each feature, reducing maintenance overhead and improving clarity.

**Documentation Policy Note:**
- All changes to module APIs (function additions, renames, deprecations) must trigger an immediate review and update of `docs/codebase_overview.md`, `docs/file_structure.md`, and the relevant `docs/src/[module].py.md`. This is a mandatory part of the Definition of Done for any API-altering task.

## config_parser.py

**Location:** src/config_parser.py

**Purpose:**
Loads and validates YAML configuration files for trading strategies. Ensures all required fields are present and the configuration is properly formatted.

**Key Function:**
- `load_config(filepath: str, validate_schema: bool = True) -> dict`
    - **filepath**: Path to the YAML config file.
    - **validate_schema**: Optional boolean (default True) to control schema validation. When False, only loads the YAML without validation.
    - **Returns**: Dict containing the parsed configuration.
    - **Raises**: FileNotFoundError if the file does not exist, ValueError if YAML is invalid or required fields are missing.
    - **Logging**: Logs errors for missing files, invalid YAML, and missing required fields. All log messages use standard error types for testability and observability.

**Example Usage:**
```python
from src import config_parser

try:
    config = config_parser.load_config('configs/strategies/sma_cross.yaml')
    print(config)
    
    # Load without schema validation if needed
    config_unvalidated = config_parser.load_config('configs/strategies/sma_cross.yaml', validate_schema=False)
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
```

**Testing:**
- Unit tests in `tests/test_config_parser.py` cover loading valid configs, handling missing files, handling invalid YAML, and handling missing required fields.
- Tests verify both function behavior and appropriate logging of events using pytest's `caplog` fixture.

## strategies.py

**Location:** src/strategies.py

**Purpose:**
This module contains the logic for different trading strategies. It implements the Strategy Pattern with a BaseStrategy abstract base class that concrete strategy classes inherit from.

**Key Classes:**
- `BaseStrategy`
    - **Purpose:** Abstract base class for all strategy implementations.
    - **Abstract Methods:**
        - `generate_signals(df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series`: Generates trading signals for a given DataFrame and parameters.
        - `get_required_parameters() -> List[str]`: Returns the list of required parameters for the strategy.
    - **Concrete Methods:**
        - `validate_parameters(params: Dict[str, Any]) -> None`: Validates that all required parameters are present.

- `SMACrossoverStrategy`
    - **Purpose:** Implements the SMA crossover strategy (inherits from BaseStrategy).
    - **Required Parameters:** 'fast_sma' and 'slow_sma'.
    - **Signal Logic:** BUY when short SMA crosses above long SMA, SELL when short SMA crosses below long SMA.

**Key Functions:**
- `generate_sma_crossover_signals(df_with_features: pd.DataFrame, short_window_col: str = "SMA_short", long_window_col: str = "SMA_long") -> pd.Series`
    - **Purpose:** Generates trading signals based on SMA crossovers (kept for backward compatibility).
    - **Returns:** Series with trading signals (1 for buy, -1 for sell, 0 for hold).
    - **Raises:** ValueError if required columns are missing.
    - **Note:** Internally uses the SMACrossoverStrategy class.

- `apply_strategy(df: pd.DataFrame, strategy_params: dict) -> pd.DataFrame`
    - **Purpose:** Applies a trading strategy to a DataFrame and generates buy/sell signals.
    - **Parameters:**
        - `df`: DataFrame containing price data and technical indicators.
        - `strategy_params`: Dictionary containing strategy type and parameters.
    - **Returns:** DataFrame with added 'signal' column (1 for buy, -1 for sell, 0 for hold).
    - **Raises:** ValueError if strategy type is not supported or required parameters are missing.
    - **Supported Strategy Types:** 
        - 'sma_crossover' (requires 'fast_sma' and 'slow_sma' parameters)
    - **Design Pattern:** Uses the Strategy Pattern to dynamically instantiate and use strategy objects based on strategy_type.

**Example Usage:**
```python
import pandas as pd
from src.strategies import generate_sma_crossover_signals, apply_strategy

# Example with generate_sma_crossover_signals
df = pd.DataFrame({
    'Close': [100, 102, 104, 103, 101],
    'SMA5': [101, 102, 103, 102.5, 102],
    'SMA20': [100, 100.5, 101, 101.5, 102]
})
signals = generate_sma_crossover_signals(df, 'SMA5', 'SMA20')
print(signals)

# Example with apply_strategy
strategy_params = {
    'strategy_type': 'sma_crossover',
    'parameters': {
        'fast_sma': 'SMA5',
        'slow_sma': 'SMA20'
    }
}
result_df = apply_strategy(df, strategy_params)
print(result_df)
```

**Testing:**
- Unit tests in `tests/test_strategies.py` verify the functionality of the `BaseStrategy` class and the `generate_sma_crossover_signals` function.
- Comprehensive unit tests in `tests/test_apply_strategy.py` verify the functionality of the `apply_strategy` function, including:
  - Correct signal generation for SMA crossover strategy
  - Proper handling of valid and invalid strategy_params (missing keys, incorrect types)
  - Behavior with different fast_sma and slow_sma column names
  - Error handling for unsupported strategy types
  - Edge cases (empty DataFrame, DataFrame with NaNs in feature columns)
  - Appropriate logging behavior
  - Preservation of the original DataFrame
- These tests ensure the reliability and correctness of the strategy application logic, providing confidence in backtesting results.

## backtester.py

**Location:** src/backtester.py

**Purpose:**
Provides a complete simulation framework for backtesting long-only trading strategies based on generated signals. Implements position tracking, trade execution, and portfolio valuation over time with both basic and enhanced tracking capabilities for detailed portfolio analytics.

**Key Functions:**
- `run_backtest(df_with_signals: pd.DataFrame, initial_capital: float, signal_col: str = 'Signal', price_col: str = 'Close') -> tuple[list[dict], pd.Series]`
    - **Primary interface as specified in design.md.**
    - Simulates long-only trading based on signals in the DataFrame.
    - **Trading Logic:** Signal=1 for buy (ignored if already in position), Signal=-1 for sell (ignored if no position), Signal=0 for hold.
    - **Returns:** Tuple of completed trade log (list of dict with buy_price, sell_price, shares, profit) and portfolio values (pd.Series indexed to input DataFrame).
    - **Raises:** ValueError if required columns are missing.
    - **Portfolio Tracking:** Calculates portfolio value as cash + (shares × current_price) for each row.
    - **Position Management:** Buys maximum shares with available cash, sells entire position on sell signal.
    - **Logging:** Structured logging with debug messages for buy/sell actions.

- `run_backtest_enhanced(df_with_signals: pd.DataFrame, initial_capital: float, signal_col: str = 'Signal', price_col: str = 'Close') -> tuple[list[dict], PortfolioData]`
    - **Enhanced backtesting with detailed portfolio composition and analytics.**
    - Same trading logic as basic version but returns comprehensive PortfolioData structure.
    - **Enhanced Features:** Portfolio composition tracking (cash vs equity percentages with exact 0% cash/100% equity when in position, 100% cash/0% equity otherwise), period and cumulative return calculations, running drawdown analysis from portfolio peaks, detailed time-series data for all metrics.
    - **Returns:** Tuple of trade log and PortfolioData NamedTuple with 9 portfolio tracking components.

**Data Structures:**
- `PortfolioData(NamedTuple)`: Enhanced portfolio data structure with portfolio_values, cash_values, equity_values, cash_pct, equity_pct, period_returns, cumulative_returns, running_drawdown, peak_values.

**Architecture:**
- **Shared Core Logic:** `_process_trading_signals()` handles common trading logic for both basic and enhanced modes.
- **Modular Design:** `_calculate_portfolio_metrics()` provides reusable metric calculations.
- **Backward Compatibility:** Original `run_backtest()` API remains unchanged.
- **Type Safety:** Uses NamedTuple for structured data and comprehensive type hints.

**Implementation Status:** ✅ Complete (Tasks 18, 19, 20, 21 & 22) - Fully implemented with enhanced portfolio tracking capabilities and 22 comprehensive tests covering all trading scenarios, portfolio analytics, and edge cases. Full trade execution simulation, comprehensive trade logging, and complete test coverage achieved.
