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
    - Dictionary containing calculated metrics with keys:
        - `'total_return_pct'`: Total return as percentage
        - `'annualized_return_pct'`: Annualized return as percentage
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
✅ **COMPLETE** - Task 23 implementation with comprehensive TDD methodology

### Task 23 Features Implemented
- ✅ Total return percentage calculation
- ✅ Annualized return percentage calculation with datetime support
- ✅ Input validation and error handling
- ✅ Formatted console output functionality
- ✅ Comprehensive test coverage (16 tests)
- ✅ Edge case handling (zero duration, empty data, negative values)

### Upcoming Features (Tasks 24-26)
- **Task 24:** Drawdown metrics (max drawdown) and trade metrics (win rate, trade count)
- **Task 25:** Risk/reward metrics (Sharpe ratio, profit factor)
- **Task 26:** Expanded test coverage for all metrics

## Test Coverage
The implementation includes comprehensive tests for:

### Basic Functionality
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
```

## Dependencies
- **pandas:** For time-series data handling and datetime operations
- **typing:** For type hints and documentation
- **Standard Library:** No external dependencies beyond pandas

## File Integration
- **Input Sources:** Compatible with `src/backtester.py` output format
- **Output Format:** Dictionary structure suitable for `main.py` orchestration
- **Test Integration:** Full pytest test suite in `tests/test_metrics.py`
