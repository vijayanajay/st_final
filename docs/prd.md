## PRD: Simple Stock Strategy Backtester (S3B)

**Author:** (You, inspired by K. Nadh)
**Version:** 0.1
**Date:** October 26, 2023

**Guiding Principles (The Kailash Nadh Mindset):**
*   **Simplicity Over Complexity:** If it can be done simply, do it simply. Avoid over-engineering.
*   **Functionality First:** Get the core working. Polish later, if ever needed.
*   **Minimalism:** Only what's necessary. No fluff.
*   **Pragmatism:** Use the right tools for the job, but don't get bogged down in tool selection.
*   **No Magic:** Clear, understandable code and processes.

### 1. Introduction
S3B is a lightweight Python tool designed to fetch historical stock data, generate basic financial features, and backtest a simple trading strategy defined in a configuration file. The initial focus is on Indian stocks, starting with Reliance Industries (RELIANCE.NS), using daily (or longer) data. The tool prioritizes extreme simplicity in implementation and user interaction.

### 2. Goals
*   To provide a barebones framework for testing long-term trading strategy ideas on historical stock data.
*   To demonstrate a simple, configurable backtesting workflow.
*   To achieve this with minimal code, minimal dependencies, and minimal user input.

### 3. Target Users
*   Individual developers/hobbyists interested in basic quantitative finance.
*   Users who prefer simple, scriptable tools over complex platforms.

### 4. User Interaction
The user will run a Python script, providing two pieces of information:
1.  The stock ticker symbol (e.g., `RELIANCE.NS`).
2.  The path to a strategy configuration file.

Example (conceptual, not a CLI command):
`python run_backtest.py --stock RELIANCE.NS --config strategy_sma_cross.yaml`
*(Self-correction: The request said "no CLI". This means the script itself will likely hardcode these or take them as direct function arguments if wrapped in a simple script. For maximum simplicity, the script might even have these as constants at the top, and the user edits the script directly for these two inputs. Let's go with user editing constants in the script for ultimate simplicity for v0.1).*

**Revised User Interaction for v0.1:**
User edits two constants at the top of the main Python script:
*   `STOCK_TICKER = "RELIANCE.NS"`
*   `STRATEGY_CONFIG_PATH = "configs/sma_cross.yaml"`
Then, the user simply executes `python main.py`.

### 5. Functional Requirements

**5.1. Data Fetching (Module: `data_loader.py`)**
*   **Source:** `yfinance` library.
*   **Stock:** Initially, hardcoded or easily changeable to `RELIANCE.NS`.
*   **Data Granularity:** `1d` (daily). No intraday data.
*   **Period:** "max" available historical data from `yfinance`. (If `yfinance` limits, then whatever is the maximum it provides for the given stock and interval).
*   **Output:** Pandas DataFrame with columns: `Date` (index), `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`.

**5.2. Feature Factory (Module: `feature_generator.py`)**
*   **Input:** Pandas DataFrame from Data Fetching.
*   **No External TA Libraries:** All features must be calculated using basic pandas/numpy operations.
*   **Output:** Pandas DataFrame with original data plus new feature columns.
*   **Initial Features to Implement:**
    *   `SMA_short`: Simple Moving Average (window defined in strategy config).
    *   `SMA_long`: Simple Moving Average (window defined in strategy config).
    *   `Price_Change_Pct_1d`: `(Close - Close.shift(1)) / Close.shift(1) * 100`
    *   `Volatility_Nday`: Rolling standard deviation of `Price_Change_Pct_1d` over N days (e.g., N=20, configurable or fixed for now).
    *   *Future (optional, if trivial):* Day of week, month.

**5.3. Strategy Configuration (File: e.g., `configs/sma_cross.yaml`)**
*   **Format:** Simple YAML or INI file. YAML is preferred for readability.
*   **Content:**
    *   `strategy_name: sma_crossover`
    *   `parameters:`
        *   `short_window: 20`  // For SMA_short
        *   `long_window: 50`   // For SMA_long
*   The system must parse this file to get strategy type and parameters.

**5.4. Strategy Implementation (Module: `strategies.py`)**
*   **SMA Crossover Logic:**
    *   **Signal Generation:**
        *   Buy Signal: When `SMA_short` crosses above `SMA_long`.
        *   Sell Signal: When `SMA_short` crosses below `SMA_long`.
    *   **Execution:**
        *   Assume trades execute at the `Close` price of the day the signal is generated.
        *   Hold one position at a time (long only). If a buy signal occurs while holding, do nothing. If a sell signal occurs while not holding, do nothing.
*   This module will contain a function for each strategy (e.g., `execute_sma_crossover(data_with_features, params)`).

**5.5. Backtester (Module: `backtester.py`)**
*   **Input:** Pandas DataFrame with features and signals.
*   **Logic:**
    *   Iterate through the data day by day.
    *   Simulate trades based on signals.
    *   Track portfolio value (assume starting capital, e.g., 100,000 INR).
    *   No transaction costs or slippage for simplicity in v0.1.
*   **Output:** A log of trades and a series of portfolio values over time.

**5.6. Performance Metrics (Module: `metrics.py`)**
*   **Input:** Trade log, portfolio value series.
*   **Metrics to Calculate & Display (clearly, to console):**
    *   Total Return (%)
    *   Annualized Return (%)
    *   Max Drawdown (%)
    *   Number of Trades
    *   Win Rate (%) (Number of profitable trades / Total trades)
    *   Average Win (%)
    *   Average Loss (%)
    *   Profit Factor (Gross Profit / Gross Loss)
    *   Sharpe Ratio (Assume risk-free rate of 0% for simplicity, or a fixed small % like 4%)

### 6. Non-Functional Requirements
*   **Simplicity of Implementation:** Code should be straightforward, easy to understand, and maintain. Minimal classes, procedural where it makes sense.
*   **Minimal Dependencies:** `python`, `pandas`, `numpy`, `yfinance`, `pyyaml`.
*   **Readability:** Clean code, sensible variable names.
*   **No GUI/CLI Frameworks:** Standard Python script execution. Output to console.

### 7. Technical Stack
*   Python 3.8+
*   Pandas
*   NumPy
*   yfinance
*   PyYAML (for config parsing)

### 8. Release Criteria (for v0.1)
*   Ability to fetch `RELIANCE.NS` daily data for the maximum available period.
*   Feature factory generates `SMA_short`, `SMA_long`.
*   SMA Crossover strategy can be configured via a YAML file for `short_window` and `long_window`.
*   Backtester executes the SMA Crossover strategy.
*   All specified performance metrics are calculated and printed to the console.
*   User only needs to edit `STOCK_TICKER` and `STRATEGY_CONFIG_PATH` in the main script and run `python main.py`.

### 9. Future Considerations (Out of Scope for v0.1)
*   Support for more stocks.
*   Support for more strategies via config.
*   More features in the feature factory.
*   Basic plotting of equity curve (matplotlib).
*   Introducing transaction costs.
*   Parameter optimization (explicitly out of scope for "simple").

### 10. Out of Scope
*   Intraday data and trading.
*   Real-time data or live trading.
*   Complex financial models or machine learning.
*   Any form of GUI or sophisticated CLI.
*   Database integration.
*   Use of external TA libraries (e.g., TA-Lib).
*   Enforce Documentation-Code Synchronization via CI/Pre-Commit and Enforce File Size Limits via CI/Pre-Commit

