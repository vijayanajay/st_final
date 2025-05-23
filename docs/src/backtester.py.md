# Module: src/backtester.py

## Overview
This module provides the simulation framework for backtesting trading strategies based on generated signals. It implements a complete long-only trading simulation that tracks positions, executes trades, and calculates portfolio values over time. The module offers both basic and enhanced tracking capabilities for detailed portfolio analytics.

## Data Structures

### PortfolioData
```python
class PortfolioData(NamedTuple):
    """Enhanced portfolio data structure with composition and analytics."""
    portfolio_values: pd.Series    # Total portfolio value over time
    cash_values: pd.Series         # Cash component over time
    equity_values: pd.Series       # Equity component over time
    cash_pct: pd.Series           # Cash percentage of portfolio
    equity_pct: pd.Series         # Equity percentage of portfolio
    period_returns: pd.Series     # Period-over-period returns (%)
    cumulative_returns: pd.Series # Cumulative returns from start (%)
    running_drawdown: pd.Series   # Running drawdown from peak (%)
    peak_values: pd.Series        # Peak portfolio values
```

## Main Interfaces

### run_backtest
```python
def run_backtest(
    df_with_signals: pd.DataFrame,
    initial_capital: float,
    signal_col: str = 'Signal',
    price_col: str = 'Close'
) -> Tuple[List[Dict], pd.Series]
```
- **Purpose:** Basic trading simulation with portfolio value tracking.
- **Args:**
    - `df_with_signals`: DataFrame with at least signal and price columns.
    - `initial_capital`: Starting cash for the simulation.
    - `signal_col`: Name of the column with trading signals (default 'Signal').
    - `price_col`: Name of the column with price data (default 'Close').
- **Returns:**
    - `trade_log`: List of completed trade events, each containing buy_price, sell_price, shares, and profit.
    - `portfolio_values`: Series of portfolio values indexed to match the input DataFrame.
- **Raises:**
    - `ValueError`: If required columns are missing.

### run_backtest_enhanced
```python
def run_backtest_enhanced(
    df_with_signals: pd.DataFrame,
    initial_capital: float,
    signal_col: str = 'Signal',
    price_col: str = 'Close'
) -> Tuple[List[Dict], PortfolioData]
```
- **Purpose:** Enhanced trading simulation with detailed portfolio composition and analytics.
- **Args:** Same as `run_backtest`
- **Returns:**
    - `trade_log`: List of completed trade events (same structure as basic version).
    - `portfolio_data`: PortfolioData structure with comprehensive tracking metrics.
- **Raises:**
    - `ValueError`: If required columns are missing.
- **Enhanced Features:**
    - Portfolio composition tracking (cash vs equity percentages)
    - Period and cumulative return calculations
    - Running drawdown analysis from portfolio peaks
    - Detailed time-series data for all metrics

## Trading Logic
- **Long-Only Strategy:** Only supports buying and selling (no short positions)
- **Signal Processing:**
  - Signal = 1 (BUY_SIGNAL): Buy signal (ignored if already in position)
  - Signal = -1 (SELL_SIGNAL): Sell signal (ignored if no position held)
  - Signal = 0 (HOLD_SIGNAL): Hold signal (no action)
- **Position Management:**
  - Buys maximum shares possible with available cash
  - Sells entire position when sell signal received
  - Tracks buy price for profit calculation
- **Portfolio Tracking:**
  - Basic: Portfolio value = cash + (shares × current_price)
  - Enhanced: Comprehensive tracking including composition, returns, and drawdowns
  - Updated for each row in the input DataFrame

## Portfolio Analytics (Enhanced Mode)
- **Composition Analysis:**
  - Cash vs equity breakdown in absolute values and percentages
  - Real-time portfolio allocation tracking (exactly 0% cash/100% equity when in position, 100% cash/0% equity otherwise)
- **Returns Calculation:**
  - Period returns: Period-over-period percentage change
  - Cumulative returns: Total return from initial capital
- **Risk Metrics:**
  - Running drawdown: Percentage decline from portfolio peaks
  - Peak tracking: Highest portfolio values achieved
- **Time-Series Data:** All metrics provided as pandas Series with matching DataFrame index

## Architecture
The module follows a DRY (Don't Repeat Yourself) approach:
- **Shared Core Logic:** `_process_trading_signals()` handles common trading logic
- **Modular Design:** `_calculate_portfolio_metrics()` provides reusable metric calculations
- **Backward Compatibility:** Original `run_backtest()` API remains unchanged
- **Type Safety:** Uses NamedTuple for structured data and comprehensive type hints

## Trade Log Structure
Each completed trade in the trade log contains:
- `buy_price`: Price at which shares were purchased
- `sell_price`: Price at which shares were sold
- `shares`: Number of shares traded
- `profit`: Total profit from the trade (sell_price - buy_price) × shares

## Implementation Status
✅ **COMPLETE** - Full implementation with enhanced portfolio tracking capabilities

### Features Implemented
- ✅ Basic backtesting with trade logging and portfolio value tracking
- ✅ Enhanced backtesting with detailed portfolio analytics
- ✅ Portfolio composition tracking (cash vs equity breakdown)
- ✅ Returns calculation (period and cumulative)
- ✅ Drawdown analysis and peak tracking
- ✅ Comprehensive test coverage (22 tests)
- ✅ Backward compatibility maintained
- ✅ Refactored architecture with shared core logic

## Test Coverage
The implementation includes tests for:
- Basic position entry (single buy signal)
- Complete trade cycles (buy-sell)
- Hold signal processing
- Redundant signal handling (long-only logic)
- Multiple trade sequences
- Edge cases (empty data, open positions at end)
- Custom column names
- Trade log structure validation
- **Enhanced tracking features:**
  - Portfolio composition tracking through buy-hold-sell cycles (exact 0% cash/100% equity after buy, 100% cash/0% equity after sell)
  - Return calculations (period and cumulative)
  - Drawdown metrics and peak tracking
  - Data structure validation
  - Integration between basic and enhanced modes
