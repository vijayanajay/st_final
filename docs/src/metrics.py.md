# Module: src/metrics.py

## Overview
This module provides performance metrics calculation functionality for the Simple Stock Strategy Backtester. It analyzes trade logs and portfolio value series to compute key financial metrics including total returns and annualized returns. The module is designed to support comprehensive portfolio performance analysis with extensible architecture for additional metrics.

## Main Interfaces

### calculate_metrics
```python
def calculate_metrics(
    trade_log: List[Dict], 
    portfolio_values: pd.Series, 
    initial_capital: float, 
    risk_free_rate: float = 0.0
) -> Dict
```
- **Purpose:** Calculate performance metrics from backtesting results.
- **Args:**
    - `trade_log`: List of completed trade dictionaries from backtester
    - `portfolio_values`: Pandas Series of portfolio values over time
    - `initial_capital`: Starting capital amount for the backtest
    - `risk_free_rate`: Risk-free rate for calculations (default 0.0, reserved for future use)
- **Returns:**
    - Dictionary containing calculated metrics with keys:        - `'total_return_pct'`: Total return as percentage
        - `'annualized_return_pct'`: Annualized return as percentage
        - `'max_drawdown_pct'`: Maximum drawdown as percentage
        - `'trade_count'`: Total number of completed trades
        - `'win_rate_pct'`: Percentage of profitable trades
        - `'sharpe_ratio'`: Risk-adjusted return measure (annualized)
        - `'profit_factor'`: Ratio of gross profits to gross losses
        - `'avg_win_pct'`: Average percentage gain of winning trades
        - `'avg_loss_pct'`: Average percentage loss of losing trades
- **Raises:**
    - `ValueError`: If initial_capital is <= 0 or portfolio_values is empty
- **Features:**
    - **Total Return Calculation:** `((final_value - initial_capital) / initial_capital) * 100`
    - **Annualized Return Calculation:** Uses time-based calculation when datetime index available
    - **Smart Time Handling:** Automatically detects datetime index for proper annualization
    - **Edge Case Handling:** Returns 0% annualized return for zero-duration periods

### print_metrics
```python
def print_metrics(metrics_dict: Dict) -> None
```
- **Purpose:** Display formatted metrics to console for user review.
- **Args:**
    - `metrics_dict`: Dictionary of metric names and values from `calculate_metrics()`
- **Returns:** None (prints to console)
- **Features:**
    - **Formatted Output:** Displays metrics with 2 decimal places
    - **Professional Presentation:** Includes header and clear labeling
    - **Flexible Input:** Handles partial metric dictionaries gracefully

## Metric Calculations

### Total Return
- **Formula:** `((final_value - initial_capital) / initial_capital) * 100`
- **Purpose:** Measures overall percentage gain or loss from initial investment
- **Range:** Can be any real number (negative for losses, positive for gains)

### Annualized Return
- **Formula:** `(((final_value / initial_capital) ** (1 / years)) - 1) * 100`
- **Purpose:** Standardizes returns to annual basis for comparison across different time periods
- **Time Calculation:**
    - Uses pandas datetime index when available
    - Calculates years as `days / 365.25` to account for leap years
    - Returns 0% for zero-duration periods (same-day start and end)
- **Edge Cases:**
    - Returns 0% when no datetime information available
    - Handles single-day backtests appropriately

### Maximum Drawdown
- **Formula:** `min((portfolio_values - portfolio_values.cummax()) / portfolio_values.cummax() * 100)`
- **Purpose:** Measures the largest peak-to-trough decline in portfolio value
- **Range:** Typically negative values (0% = no drawdown, -20% = 20% decline from peak)
- **Implementation:** Uses pandas cummax() to track running peaks and calculate percentage declines

### Trade Count
- **Formula:** `len(trade_log)`
- **Purpose:** Counts total number of completed trades (buy-sell pairs)
- **Range:** Non-negative integers (0 = no trades completed)

### Win Rate
- **Formula:** `(profitable_trades / total_trades) * 100` if total_trades > 0, else 0%
- **Purpose:** Measures percentage of profitable trades out of total trades
- **Range:** 0% to 100% (50% = half of trades were profitable)
- **Implementation:** Counts trades where profit > 0, handles division by zero

### Sharpe Ratio
- **Formula:** `(mean(returns - risk_free_rate) / std(returns - risk_free_rate)) * sqrt(252)`
- **Purpose:** Measures risk-adjusted return (reward-to-variability ratio)
- **Range:** Any real number (higher = better risk-adjusted performance)
- **Implementation:** Calculates excess returns over risk-free rate, then divides by volatility
- **Annualization:** Assumes daily returns and annualizes by multiplying by square root of 252 (trading days)

### Profit Factor
- **Formula:** `sum(profits) / abs(sum(losses))` for all trades
- **Purpose:** Measures ratio of gross profits to gross losses
- **Range:** 0 to infinity (>1 indicates profitable strategy)
- **Edge Cases:**
    - Returns infinity when no losing trades (all profits)
    - Returns 0 when no winning trades or empty trade log

### Average Win/Loss Percentages
- **Formula Win:** Average of `(profit / (buy_price * shares)) * 100` for all profitable trades
- **Formula Loss:** Average of `(profit / (buy_price * shares)) * 100` for all losing trades (negative value)
- **Purpose:** Measures average percentage gain of winning trades and average percentage loss of losing trades (as a percentage of total cost basis per trade)
- **Edge Cases:** Returns 0 when no winning/losing trades or empty trade log. Skips trades with zero cost basis to avoid division by zero.

## Architecture & Design

### Input Validation
- **Capital Validation:** Ensures initial_capital > 0
- **Data Validation:** Ensures portfolio_values is not empty
- **Error Handling:** Provides clear error messages for invalid inputs

### Time-Series Intelligence
- **Automatic Detection:** Identifies datetime-indexed portfolio series
- **Flexible Calculation:** Works with both datetime and non-datetime indices
- **Precision:** Uses 365.25 days per year for accurate leap year handling

### Extensible Design
- **Modular Structure:** Each metric calculation is self-contained
- **Standard Interface:** Consistent input/output patterns for future metrics
- **Future-Ready:** Architecture supports additional metrics in upcoming tasks

## Implementation Status
✅ **COMPLETE** - Task 25 implementation with comprehensive TDD methodology

### Task 25 Features Implemented (NEW)
- ✅ Sharpe ratio calculation with annualization for risk-adjusted returns
- ✅ Profit factor calculation to measure gross profits to gross losses ratio
- ✅ Average win percentage calculation for winning trades
- ✅ Average loss percentage calculation for losing trades  
- ✅ Enhanced console output with new risk/reward metrics
- ✅ Comprehensive test coverage (62 total tests, 17 new for Task 25)
- ✅ Helper functions: `_calculate_sharpe_ratio()`, `_calculate_profit_factor()`, `_calculate_avg_win_pct()`, and `_calculate_avg_loss_pct()`

### Task 24 Features Implemented (COMPLETE)
- ✅ Maximum drawdown percentage calculation with peak-to-trough analysis
- ✅ Trade count calculation from trade log
- ✅ Win rate percentage calculation with profitable trade analysis
- ✅ Enhanced console output with new metrics formatting
- ✅ Comprehensive test coverage (28 tests for Task 24)
- ✅ Helper functions: `_calculate_max_drawdown()` and `_calculate_win_rate()`

### Task 23 Features Implemented (COMPLETE)
- ✅ Total return percentage calculation
- ✅ Annualized return percentage calculation with datetime support
- ✅ Input validation and error handling
- ✅ Formatted console output functionality
- ✅ Comprehensive test coverage (16 tests from Task 23)
- ✅ Edge case handling (zero duration, empty data, negative values)

### Upcoming Features (Task 26)
- **Task 26:** Expanded test coverage for all metrics

## Test Coverage
The implementation includes comprehensive tests for:

### Task 25 New Functionality
- **Sharpe Ratio Tests:** Positive returns, negative returns, with risk-free rate, empty returns
- **Profit Factor Tests:** All winning trades, all losing trades, mixed trades, break-even trades, empty trade log
- **Average Win/Loss Tests:** Basic calculations, no winners/losers scenarios, empty trade log scenarios
- **Integration Tests:** Full metrics calculation with all new risk/reward metrics
- **Print Formatting Tests:** Updated display with new metrics

### Task 24 Functionality
- **Maximum Drawdown Tests:** Simple decline scenarios, no drawdown cases, single value edge cases
- **Trade Count Tests:** Zero trades, multiple trades, empty trade log scenarios
- **Win Rate Tests:** No trades, all winning, all losing, mixed profits, break-even trades
- **Print Formatting Tests:** Complete metrics display, partial metrics display

### Task 23 Basic Functionality
- Total return calculation with gains, losses, and no change scenarios
- Annualized return calculation for different time periods (1 year, 2 years, single day)
- Integration with trade logs and portfolio values

### Edge Cases & Error Handling
- Empty portfolio values (raises ValueError)
- Invalid initial capital (raises ValueError)
- Zero-duration periods (returns 0% annualized)
- Non-datetime indexed series (graceful fallback)

### Console Output
- Formatted metric display testing
- Proper decimal precision (2 places)
- Header and label formatting

### Integration Testing
- Compatibility with backtester output format
- Trade log integration (though not directly used in Task 23)
- Portfolio value series from various sources

## Usage Example
```python
# After running backtest
trade_log, portfolio_values = run_backtest(df_with_signals, 10000)

# Calculate metrics
metrics = calculate_metrics(trade_log, portfolio_values, 10000)

# Display results
print_metrics(metrics)
# Output:
# === Performance Metrics ===
# Total Return: 15.23%
# Annualized Return: 8.45%
# Max Drawdown: -12.34%
# Number of Trades: 25
# Win Rate: 64.00%
# Sharpe Ratio: 1.25
# Profit Factor: 2.50
# Average Win: 12.50%
# Average Loss: -7.50%
```

## Dependencies
- **pandas:** For time-series data handling and datetime operations
- **typing:** For type hints and documentation
- **Standard Library:** No external dependencies beyond pandas

## File Integration
- **Input Sources:** Compatible with `src/backtester.py` output format
- **Output Format:** Dictionary structure suitable for `main.py` orchestration
- **Test Integration:** Full pytest test suite in `tests/test_metrics.py`
