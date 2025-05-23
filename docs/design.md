## Technical Design Document: Simple Stock Strategy Backtester (S3B)

**Version:** 1.0
**Date:** October 26, 2023
**Author:** (AI Architect, channeling Pragmatism)

### 1. Introduction & Overview

This document outlines the technical design for the Simple Stock Strategy Backtester (S3B), a Python-based tool for personal use on a Windows desktop. S3B aims to provide a minimalist framework for fetching historical stock data, generating basic financial features, and backtesting simple trading strategies defined in a configuration file.

**Goals of this Design Document:**
*   Provide a clear blueprint for the implementation of S3B, adhering to the PRD v0.1.
*   Translate product requirements into actionable technical specifications.
*   Emphasize simplicity, maintainability (for a solo developer), and correctness.
*   Ensure the design is practical for implementation by an individual.

**Non-Goals (Personal Use Constraints):**
*   **Scalability:** The system is not designed for high-volume, concurrent backtesting or massive datasets beyond what `pandas` can comfortably handle in memory for a single stock's history.
*   **Multi-User Support:** The application is intended for a single user. No user accounts, roles, or concurrent access controls are considered.
*   **High Availability/Fault Tolerance:** Standard script execution; if it fails, the user reruns it. No complex recovery mechanisms.
*   **Distributed Computing:** All processing occurs on a single machine.
*   **Web Interface/API:** The application is purely a local command-line/script-based tool.
*   **Complex GUI:** Interaction is via editing script constants and observing console output, as per PRD.
*   **Enterprise-grade Security:** Not applicable for a local, personal tool.
*   **Automated CI/CD, Advanced DevOps:** Build and deployment are manual and simple.
*   **Real-time trading or live data feeds.**

### 2. Architectural Style & Guiding Principles

**Chosen Architectural Pattern(s):**
*   **Modular, Script-Based Architecture with Layered Responsibilities:**
    *   The application will be structured as a collection of Python modules, each responsible for a distinct part of the workflow (data loading, feature generation, strategy execution, etc.), as outlined in the PRD.
    *   This can be viewed as a simple layered approach:
        1.  **Data Acquisition Layer:** (`data_loader.py`) - Fetches raw data.
        2.  **Feature Engineering Layer:** (`feature_generator.py`) - Transforms raw data into data with features.
        3.  **Strategy & Configuration Layer:** (`config_parser.py`, `strategies.py`) - Defines and applies trading logic based on configuration.
        4.  **Backtesting Engine Layer:** (`backtester.py`) - Simulates trading and tracks performance.
        5.  **Reporting Layer:** (`metrics.py`) - Calculates and presents results.
        6.  **Orchestration:** (`main.py`) - Coordinates the execution flow.
    *   **Justification:** This aligns directly with the PRD's modular structure and emphasis on simplicity. It avoids the overhead of more formal architectural patterns (like full MVC/MVVM) which are unnecessary for a console-based script. It promotes separation of concerns, making the code easier to understand, test, and maintain by a single developer.

**Core Design Principles:**
*   **Simplicity Over Complexity (KISS):** Every design choice will favor the simplest approach that meets the requirements. Avoid over-engineering.
*   **Functionality First:** Core logic will be prioritized.
*   **Minimalism (YAGNI - You Ain't Gonna Need It):** Only implement features explicitly required by the PRD for v0.1.
*   **Pragmatism:** Use appropriate Python features and libraries effectively without unnecessary abstraction.
*   **No Magic:** Code and processes should be clear and understandable.
*   **Single Responsibility Principle (SRP):** Each module and function will aim to have a single, well-defined responsibility.
*   **Don't Repeat Yourself (DRY):** Avoid code duplication where practical, through functions and well-structured modules.

### 3. Technology Stack Selection

*   **Programming Language:** **Python 3.8+**
    *   **Justification:** Explicitly required by the PRD. Ideal for data manipulation (pandas, numpy), scripting, and has the necessary libraries (`yfinance`, `PyYAML`).
*   **UI Framework/Library:** **None (Console Output)**
    *   **Justification:** Explicitly required by the PRD ("No GUI/CLI Frameworks," "Output to console"). User interaction is via editing constants in the main script.
*   **Data Persistence:**
    *   **Configuration:** YAML files (e.g., `configs/sma_cross.yaml`).
        *   **Justification:** Required by PRD, human-readable, good for structured configuration.
    *   **Application Data/Results:** Primarily console output.
        *   **Justification:** Meets PRD v0.1 requirements. For debugging or more persistent records beyond console scrollback, simple CSV/text file outputs could be trivially added later if desired by the user, but are not part of the core v0.1 design. No database is needed.
*   **Key Libraries/Dependencies:**
    *   `pandas`: For DataFrame manipulation, core data structure.
    *   `numpy`: For numerical operations, often a dependency of pandas and used for calculations.
    *   `yfinance`: For fetching historical stock data.
    *   `PyYAML`: For parsing YAML configuration files.
    *   **Justification:** All are explicitly listed in the PRD and are standard, well-supported libraries for these tasks in Python.

### 4. Detailed Component Design

The application will consist of the following Python modules:

**4.1. `main.py` (Orchestrator)**
*   **Responsibilities:**
    *   Entry point of the application.
    *   Contains user-editable constants: `STOCK_TICKER` and `STRATEGY_CONFIG_PATH`.
    *   Orchestrates the overall backtesting workflow:
        1.  Calls `config_parser` to load strategy configuration.
        2.  Calls `data_loader` to fetch historical stock data.
        3.  Calls `feature_generator` to add technical features to the data.
        4.  Calls the appropriate strategy function from `strategies` to generate trading signals.
        5.  Calls `backtester` to simulate trades and calculate portfolio values.
        6.  Calls `metrics` to compute and print performance statistics.
    *   Handles top-level error catching and reporting.
*   **Interfaces:**
    *   Not directly interfaced by other modules; it's the top-level script.
*   **Key Data Structures:** None managed directly; passes DataFrames and config objects between other components.
*   **Applicable Design Patterns:** Procedural script flow.
*   **Interaction with other components:** Calls functions from all other modules in sequence.

**4.2. `config_parser.py`**
*   **Responsibilities:**
    *   Load and parse the strategy configuration YAML file.
    *   Validate the basic structure and presence of required parameters (e.g., `strategy_name`, `parameters`, specific window sizes).
    *   Return a structured representation of the configuration (e.g., a dictionary).
*   **Interfaces:**
    *   `load_config(filepath: str, validate_schema: bool = True) -> dict:`
        *   Input: Path to the YAML configuration file, optional schema validation flag.
        *   Output: A dictionary representing the parsed configuration.
        *   Raises: `FileNotFoundError` if config file not found, `ValueError` or custom exception for invalid config format/content.
*   **Key Data Structures:** Python dictionary representing the YAML content.
*   **Applicable Design Patterns:** Simple parser.
*   **Interaction with other components:** Called by `main.py`.

**4.3. `data_loader.py`**
*   **Responsibilities:**
    *   Fetch historical stock data using the `yfinance` library.
    *   Handle parameters like stock ticker, data granularity (`1d`), and period (`max`).
    *   Support column selection and cache control.
    *   Ensure the output DataFrame has the specified columns (defaults to: `Date` (index), `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`).
*   **Interfaces:**
    *   `fetch_data(ticker: str, period: str = "max", interval: str = "1d", columns: List[str] = None, use_cache: bool = True) -> pd.DataFrame:`
        *   Input: Stock ticker symbol, period string, interval string, optional column selection, and cache control flag.
        *   Output: Pandas DataFrame with historical stock data (all columns or specified subset).
        *   Raises: `ValueError` or custom exception if data fetching fails or returns an empty/invalid DataFrame.
    *   `fetch(ticker: str, period: str = "1y", columns: List[str] = None, use_cache: bool = True) -> pd.DataFrame:`
        *   Backward-compatibility wrapper around `fetch_data`.
        *   Has a different default for `period` parameter ("1y" instead of "max").
        *   Always uses "1d" as the interval.
        *   Delegates to `fetch_data` for actual implementation.
*   **Key Data Structures:** Pandas DataFrame.
*   **Applicable Design Patterns:** Wrapper/Facade around `yfinance` API.
*   **Interaction with other components:** Called by `main.py`.

**4.4. `feature_generator.py`**
*   **Responsibilities:**
    *   Calculate financial features based on the input DataFrame.
    *   Implement features using basic pandas/numpy operations only (no external TA libraries).
    *   Add new feature columns to the DataFrame.
    *   Initial features: `SMA_short`, `SMA_long`, `Price_Change_Pct_1d`, `Volatility_Nday`.
*   **Interfaces:**
    *   `add_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:`
        *   Calculates SMA for the specified column and window, returning a Series named 'sma_{window}'.
    *   `add_price_change_pct_1d(df: pd.DataFrame, column: str = "close") -> pd.Series:`
        *   Calculates 1-day percentage price change for the specified column, returning a Series named 'price_change_pct_1d'.
    *   `add_volatility_nday(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series:`
        *   Calculates N-day rolling std dev of price changes for the specified column and window, returning a Series named 'volatility_{window}'.
    *   `generate_features(df: pd.DataFrame, feature_config: dict) -> pd.DataFrame:`
        *   Orchestrator function within this module.
        *   Input: DataFrame from `data_loader`, feature configuration dictionary.
        *   Output: DataFrame with original data + new feature columns.
        *   This function iterates through the feature_config dictionary where keys are feature names (e.g., "sma", "price_change_pct_1d", "volatility_nday") and values are their parameters. For each feature, it calls the corresponding add_* function with the provided parameters.
        *   This design provides more flexibility than coupling directly to strategy parameters, as it allows any combination of features to be generated based on the configuration, regardless of the strategy that will use them.
        *   Example feature_config structure:
          ```python
          {
              "sma": {"column": "close", "window": 20},
              "price_change_pct_1d": {"column": "close"},
              "volatility_nday": {"column": "close", "window": 20}
          }
          ```
*   **Key Data Structures:** Pandas DataFrame.
*   **Applicable Design Patterns:** Functions act as simple feature calculators.
*   **Interaction with other components:** Called by `main.py`. Takes DataFrame and strategy parameters.

**4.5. `strategies.py`**
*   **Responsibilities:**
    *   Implement the logic for generating trading signals based on features.
    *   Currently, only SMA Crossover strategy.
    *   Adhere to execution rules: trades at `Close` of signal day, long only, one position at a time.
*   **Interfaces:**
    *   `generate_sma_crossover_signals(df_with_features: pd.DataFrame, short_window_col: str, long_window_col: str) -> pd.DataFrame:`
        *   Input: DataFrame with `SMA_short` and `SMA_long` columns (names passed as `short_window_col`, `long_window_col`).
        *   Output: DataFrame with new columns: `Signal` (e.g., 1 for Buy, -1 for Sell, 0 for Hold/Nothing).
        *   Logic:
            *   Buy: `SMA_short` crosses above `SMA_long`.
            *   Sell: `SMA_short` crosses below `SMA_long`.
            *   Ensure only one signal type per day (buy or sell).
            *   Handle initial period where SMAs are NaN.
*   **Key Data Structures:** Pandas DataFrame.
*   **Applicable Design Patterns:** **Strategy Pattern** (simple form). The module contains functions, each representing a strategy's signal generation logic. `main.py` would select which function to call based on `strategy_name` from config. For v0.1, it's hardcoded to call the SMA crossover.
*   **Interaction with other components:** Called by `main.py`. Takes DataFrame with features.

**4.6. `backtester.py`**
*   **Responsibilities:**
    *   Simulate trading based on signals from the strategy module.
    *   Iterate through data day by day.
    *   Track portfolio value (assume fixed starting capital).
    *   Implement "long only, one position at a time" logic.
    *   No transaction costs or slippage for v0.1.
    *   Provide enhanced portfolio analytics including composition, returns, and drawdown tracking.
*   **Interfaces:**
    *   `run_backtest(df_with_signals: pd.DataFrame, initial_capital: float, signal_col: str = 'Signal', price_col: str = 'Close') -> tuple[list[dict], pd.Series]:`
        *   Input: DataFrame with features and a `Signal` column, initial capital.
        *   Output:
            *   `trade_log`: A list of dictionaries, where each dictionary represents a completed trade (e.g., `{'buy_price': float, 'sell_price': float, 'shares': float, 'profit': float}`).
            *   `portfolio_values`: A Pandas Series representing the portfolio value over time, indexed to match the input DataFrame.
        *   Raises: `ValueError` if required columns are missing.
    *   `run_backtest_enhanced(df_with_signals: pd.DataFrame, initial_capital: float, signal_col: str = 'Signal', price_col: str = 'Close') -> tuple[list[dict], PortfolioData]:`
        *   Input: Same as `run_backtest`.
        *   Output:
            *   `trade_log`: Same trade log structure as `run_backtest`.
            *   `portfolio_data`: A `PortfolioData` NamedTuple containing comprehensive portfolio analytics.
        *   Purpose: Enhanced backtesting with detailed portfolio composition tracking, returns analysis, and drawdown metrics.
        *   Raises: `ValueError` if required columns are missing.
*   **Key Data Structures:**
    *   `PortfolioData(NamedTuple)`: Enhanced portfolio data structure containing:
        *   `portfolio_values`: pd.Series - Total portfolio value over time
        *   `cash_values`: pd.Series - Cash component over time
        *   `equity_values`: pd.Series - Equity component over time  
        *   `cash_pct`: pd.Series - Cash percentage of portfolio
        *   `equity_pct`: pd.Series - Equity percentage of portfolio
        *   `period_returns`: pd.Series - Period-over-period returns (%)
        *   `cumulative_returns`: pd.Series - Cumulative returns from start (%)
        *   `running_drawdown`: pd.Series - Running drawdown from peak (%)
        *   `peak_values`: pd.Series - Peak portfolio values achieved
    *   Internal state: `current_position` (bool), `entry_price` (float), `shares_held` (float), `cash` (float), `portfolio_value` (float).
    *   Trade log structure: List of dictionaries with keys: `buy_price`, `sell_price`, `shares`, `profit`.
*   **Applicable Design Patterns:** 
    *   Simulation loop for trade execution.
    *   Shared core logic pattern with `_process_trading_signals()` internal function.
    *   Modular design with `_calculate_portfolio_metrics()` for reusable calculations.
*   **Interaction with other components:** Called by `main.py`. Takes DataFrame with signals.

**4.7. `metrics.py`**
*   **Responsibilities:**
    *   Calculate performance metrics based on the trade log and portfolio value series.
    *   Metrics: Total Return (%), Annualized Return (%), Max Drawdown (%), Number of Trades, Win Rate (%), Average Win (%), Average Loss (%), Profit Factor, Sharpe Ratio (assume 0% risk-free rate or fixed small %).
    *   Format and print these metrics clearly to the console.
*   **Interfaces:**
    *   `calculate_metrics(trade_log: list[dict], portfolio_values: pd.Series, initial_capital: float, risk_free_rate: float = 0.0) -> dict:`
        *   Input: Trade log, portfolio value series, initial capital, risk-free rate (default 0).
        *   Output: A dictionary containing all calculated metric names and their values.
    *   `print_metrics(metrics_dict: dict) -> None:`
        *   Input: Dictionary of metrics.
        *   Output: Prints formatted metrics to the console.
*   **Key Data Structures:** Dictionary of metrics.
*   **Applicable Design Patterns:** Collection of calculation functions.
*   **Interaction with other components:** Called by `main.py`. Takes outputs from `backtester.py`.

### 5. Data Model & Persistence

*   **Primary Data Structures:**
    *   **Historical Stock Data:** Pandas DataFrame. Schema: `Date` (DatetimeIndex), `Open` (float), `High` (float), `Low` (float), `Close` (float), `Adj Close` (float), `Volume` (int/float).
    *   **Data with Features:** Pandas DataFrame, extending historical data with columns like `SMA_short` (float), `SMA_long` (float), `Price_Change_Pct_1d` (float), `Volatility_Nday` (float).
    *   **Data with Signals:** Pandas DataFrame, extending data with features with a `Signal` column (int: 1 for buy, -1 for sell, 0 for hold).
    *   **Strategy Configuration:** Python dictionary parsed from YAML. Example structure from PRD:
        ```yaml
        strategy_name: sma_crossover
        parameters:
          short_window: 20
          long_window: 50
        # Potentially:
        # volatility_window: 20 # If made configurable
        ```
    *   **Trade Log:** List of dictionaries. Each dict: `{'entry_date': datetime, 'entry_price': float, 'exit_date': datetime, 'exit_price': float, 'shares': float, 'profit_abs': float, 'profit_pct': float}`.
    *   **Portfolio Values:** Pandas Series, indexed by Date, values are portfolio total value (float).

*   **Data Persistence:**
    *   **Input Configuration:** Read from `.yaml` file specified by `STRATEGY_CONFIG_PATH`.
    *   **Output Data:** All results (trade log details, portfolio summary, metrics) are printed to the console as per PRD v0.1. No file-based persistence of results is required for v0.1.
        *   *Consideration for user:* If the user wants to save trade logs or portfolio values, they can redirect console output or minor code additions could save these to CSV. This is outside v0.1 scope.

*   **Data Validation:**
    *   **Configuration File:** `config_parser.py` will check for:
        *   File existence.
        *   Presence of `strategy_name` and `parameters`.
        *   For `sma_crossover`, presence and valid integer types for `short_window`, `long_window`.
        *   Window values must be positive and `short_window` < `long_window`.
    *   **Fetched Data:** `data_loader.py` will check if the DataFrame returned by `yfinance` is not empty.
    *   **Feature Calculation:** Ensure input DataFrame has necessary columns (e.g., `Close` for SMA).
    *   **Enforcement:** Validations will occur at the beginning of the respective module functions. Errors will raise Python exceptions (e.g., `ValueError`, `FileNotFoundError`).

*   **Backup/Restore Considerations:**
    *   The user is responsible for backing up their Python scripts (`.py` files) and strategy configuration files (`.yaml`).
    *   Since no application data is persisted to disk by default, there's no application-specific backup/restore mechanism needed.

### 6. User Interface (UI) / User Experience (UX) Flow (Technical Perspective)

1.  **Configuration:** User opens `main.py` in a text editor.
2.  User modifies the `STOCK_TICKER` (e.g., `"RELIANCE.NS"`) and `STRATEGY_CONFIG_PATH` (e.g., `"configs/sma_cross.yaml"`) constants at the top of `main.py`.
3.  User ensures the YAML configuration file (e.g., `configs/sma_cross.yaml`) exists and is correctly formatted with strategy parameters.
4.  **Execution:** User opens a terminal/command prompt, navigates to the script's directory, and runs `python main.py`.
5.  **Processing (Internal Flow):**
    *   `main.py` reads constants.
    *   `config_parser.py` loads and validates `sma_cross.yaml`.
    *   `data_loader.py` fetches stock data for `STOCK_TICKER`.
    *   `feature_generator.py` calculates SMAs (and other defined features) using parameters from the config.
    *   `strategies.py` generates buy/sell signals based on the SMA crossover logic.
    *   `backtester.py` simulates trades using these signals and an initial capital (e.g., 100,000 hardcoded in `main.py` or `backtester.py`). It generates a trade log and portfolio value series.
    *   `metrics.py` calculates performance metrics from the backtest results.
6.  **Output:** `metrics.py` (via `main.py`) prints all specified performance metrics to the console in a readable format. The backtester might also print a summary of trades or key trade details if deemed useful for v0.1 (PRD mentions "A log of trades" as output from backtester, which could be printed or just passed to metrics). For v0.1, let's assume the detailed trade log is primarily for metric calculation, and console output focuses on summary metrics. A few example trades could be printed for verbosity if desired.

### 7. Error Handling & Logging Strategy

*   **Error Handling:**
    *   Standard Python exceptions will be used (`try...except` blocks).
    *   File I/O errors (e.g., config file not found) will raise `FileNotFoundError`.
    *   Data fetching issues (e.g., invalid ticker, network problem) will be caught, and an informative error message printed. `yfinance` might raise its own exceptions.
    *   Invalid configuration (e.g., missing keys, bad values) will raise `ValueError` or custom exceptions from `config_parser.py`.
    *   Calculation errors (e.g., division by zero if not handled in feature/metric calculations, though pandas often handles this with `NaN`/`inf`) should be caught or lead to clear Python tracebacks.
    *   All unhandled exceptions will result in a Python traceback printed to the console, which is acceptable for a personal development tool.
    *   User-facing error messages printed to the console will be clear and actionable where possible (e.g., "Error: Config file 'path/to/config.yaml' not found.").

*   **Logging Strategy:**
    *   For v0.1, primary output is to the console.
    *   Python's built-in `print()` function will be sufficient for status messages (e.g., "Fetching data for RELIANCE.NS...", "Calculating features...", "Running backtest...", "Performance Metrics:") and final results.
    *   No separate file-based logging is planned for v0.1 to maintain simplicity. If debugging becomes complex, the developer (user) can temporarily add more `print` statements or introduce the `logging` module minimally.

### 8. Testing Strategy (TDD-focused)

*   **Commitment to TDD:** Development will adhere to a Test-Driven Development (TDD) approach. Tests will be written before the corresponding application code. The cycle will be Red (write a failing test) -> Green (write minimal code to pass the test) -> Refactor (improve the code while keeping tests green).

*   **Unit Tests:**
    *   **`config_parser.py`:**
        *   Test loading valid YAML.
        *   Test handling of missing files.
        *   Test handling of malformed YAML.
        *   Test validation of required keys and data types (e.g., `short_window` is int).
    *   **`data_loader.py`:**
        *   Mock `yfinance.Ticker(...).history(...)` calls.
        *   Test correct DataFrame structure and columns for successful fetch.
        *   Test handling of `yfinance` errors or empty data returns.
    *   **`feature_generator.py`:**
        *   For each feature function (e.g., `add_sma`, `add_price_change_pct_1d`):
            *   Provide sample input DataFrames (e.g., created manually or from small CSVs).
            *   Assert correct calculation of feature values.
            *   Verify correct handling of edge cases (e.g., NaNs at the beginning of SMA calculations).
    *   **`strategies.py` (`generate_sma_crossover_signals`):**
        *   Provide sample DataFrames with feature columns.
        *   Test correct signal generation for:
            *   Buy crossover (`SMA_short` > `SMA_long` after being <=).
            *   Sell crossover (`SMA_short` < `SMA_long` after being >=).
            *   No signal / hold conditions.
            *   Consecutive signals (ensure only first signal of a new state is taken if trades are discrete).
    *   **`backtester.py`:**
        *   Test with predefined DataFrames containing prices and signals.
        *   Verify correct trade execution (entry/exit prices, number of shares based on capital).
        *   Verify "long only, one position at a time" logic.
        *   Verify correct calculation of portfolio value series over time.
        *   Test with no trades, a single trade, multiple trades.
        *   Test trade log structure and content.
    *   **`metrics.py`:**
        *   For each metric:
            *   Provide sample trade logs and portfolio value series.
            *   Assert correct calculation of the metric.
            *   Test edge cases (e.g., no trades, all winning trades, all losing trades, zero division for profit factor).
            *   Test Sharpe ratio with different risk-free rates (including default 0).

*   **Integration/Component Tests (Minimal):**
    *   A test for `main.py`'s orchestration logic:
        *   Use a small, static CSV file as a data source (mocking `data_loader.py` or having it read a local file for testing).
        *   Use a fixed, simple strategy configuration.
        *   Run the main workflow and assert that final metrics are within an expected range or match pre-calculated values for this static dataset. This ensures components connect correctly.

*   **Testing Framework(s):**
    *   **`pytest`** will be used as the testing framework.
    *   **Justification:** `pytest` offers a simple, yet powerful way to write tests, with good support for fixtures, assertions, and test discovery. It's less boilerplate than `unittest`.
    *   Mocking can be done using `unittest.mock.patch` (part of Python's standard library) or `pytest-mock` plugin.

### 9. Build & Deployment (for Personal Use)

*   **Build Process:**
    *   No formal "build" process in the compiled sense.
    *   The application is a set of Python scripts.
    *   A `requirements.txt` file will be provided:
        ```
        pandas
        numpy
        yfinance
        PyYAML
        pytest  # For development/testing
        ```
*   **Deployment Strategy (User Setup):**
    1.  User ensures Python 3.8+ is installed on their Windows machine and added to PATH.
    2.  User clones or downloads the S3B script files (e.g., `main.py`, `data_loader.py`, etc., and `configs/` directory) to a local folder.
    3.  User opens a command prompt/terminal in that folder.
    4.  User creates a virtual environment (recommended):
        `python -m venv venv`
        `venv\Scripts\activate`
    5.  User installs dependencies:
        `pip install -r requirements.txt`
    6.  User edits `STOCK_TICKER` and `STRATEGY_CONFIG_PATH` in `main.py` as needed.
    7.  User runs the backtester:
        `python main.py`

### 10. Future Considerations (from PRD & Design)

*   **Support for more stocks:** Currently, `STOCK_TICKER` is a single string. Could be extended to a list, and `main.py` could loop through them.
*   **Support for more strategies:** `strategies.py` can have more functions. `main.py` and `config_parser.py` would need to dynamically select the strategy function based on `strategy_name` in the config.
*   **More features in `feature_generator.py`:** New functions can be added. The `generate_features` orchestrator in this module might need to become more config-driven.
*   **Basic plotting:** `matplotlib` could be added to plot equity curve and SMA crossovers. This would be a significant UX improvement but adds a dependency.
*   **Transaction costs/slippage:** `backtester.py` logic would need to be updated to subtract costs from trades and adjust execution prices for slippage.
*   **Saving results to file:** Instead of console-only, `metrics.py` or `main.py` could write results (metrics, trade log) to CSV or JSON files.
*   **Known Limitations:**
    *   Single stock processing per run (by v0.1 design).
    *   Strategy logic (SMA crossover) is mostly hardcoded in the workflow; only parameters are from config.
    *   Performance is dependent on pandas; very long histories or extremely numerous features might slow down on low-spec machines (but generally fine for daily data).
    *   Error handling is basic; focuses on clear messages rather than complex recovery.

