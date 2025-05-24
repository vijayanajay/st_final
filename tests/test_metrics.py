"""
Tests for metrics.py module.
Task 23: Create metrics.py with basic return calculations (Total Return % and Annualized Return %)
"""
import pytest
import pandas as pd
import numpy as np
from src import metrics


def test_calculate_metrics_exists():
    """Test that calculate_metrics function exists."""
    assert hasattr(metrics, 'calculate_metrics'), "calculate_metrics function must exist in metrics.py"


def test_calculate_metrics_total_return_simple_gain():
    """Test total return calculation with simple portfolio gain."""
    # Arrange: Portfolio that gained 20% (1000 -> 1200)
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1200.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert isinstance(result, dict), "calculate_metrics should return a dictionary"
    assert 'total_return_pct' in result, "Result should contain total_return_pct"
    assert result['total_return_pct'] == 20.0, "Should calculate 20% total return"


def test_calculate_metrics_total_return_simple_loss():
    """Test total return calculation with portfolio loss."""
    # Arrange: Portfolio that lost 15% (1000 -> 850)
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 850.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['total_return_pct'] == -15.0, "Should calculate -15% total return"


def test_calculate_metrics_total_return_no_change():
    """Test total return calculation with no portfolio change."""
    # Arrange: Portfolio unchanged (1000 -> 1000)
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1000.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['total_return_pct'] == 0.0, "Should calculate 0% total return"


def test_calculate_metrics_annualized_return_one_year():
    """Test annualized return calculation over exactly one year."""
    # Arrange: 44% return over exactly 1 year should be 44% annualized
    initial_capital = 1000.0
    start_date = pd.Timestamp('2022-01-01')
    end_date = pd.Timestamp('2023-01-01')  # Exactly 1 year later
    portfolio_values = pd.Series([1000.0, 1440.0], 
                                index=[start_date, end_date])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert 'annualized_return_pct' in result, "Result should contain annualized_return_pct"
    assert abs(result['annualized_return_pct'] - 44.0) < 0.1, "Should calculate ~44% annualized return for 1 year"


def test_calculate_metrics_annualized_return_two_years():
    """Test annualized return calculation over two years."""
    # Arrange: 44% return over 2 years should be ~20% annualized
    # Formula: (1.44)^(1/2) - 1 = 0.2 = 20%
    initial_capital = 1000.0
    start_date = pd.Timestamp('2022-01-01')
    end_date = pd.Timestamp('2024-01-01')  # Exactly 2 years later
    portfolio_values = pd.Series([1000.0, 1440.0], 
                                index=[start_date, end_date])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    expected_annualized = ((1440.0 / 1000.0) ** (1.0 / 2.0) - 1.0) * 100.0  # ~20%
    assert abs(result['annualized_return_pct'] - expected_annualized) < 0.1, "Should calculate correct annualized return"


def test_calculate_metrics_annualized_return_single_day():
    """Test annualized return calculation for single day (edge case)."""
    # Arrange: Same day start and end
    initial_capital = 1000.0
    same_date = pd.Timestamp('2022-01-01')
    portfolio_values = pd.Series([1000.0, 1200.0], 
                                index=[same_date, same_date])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert: For zero duration, annualized return should be 0
    assert result['annualized_return_pct'] == 0.0, "Should return 0% annualized return for zero time period"


def test_print_metrics_exists():
    """Test that print_metrics function exists."""
    assert hasattr(metrics, 'print_metrics'), "print_metrics function must exist in metrics.py"


def test_calculate_metrics_docstring():
    """Test that calculate_metrics has a meaningful docstring."""
    assert metrics.calculate_metrics.__doc__ is not None and len(metrics.calculate_metrics.__doc__) > 10, \
        "calculate_metrics should have a meaningful docstring"


def test_print_metrics_docstring():
    """Test that print_metrics has a meaningful docstring."""
    assert metrics.print_metrics.__doc__ is not None and len(metrics.print_metrics.__doc__) > 10, \
        "print_metrics should have a meaningful docstring"


# Additional edge case tests for robust implementation

def test_calculate_metrics_empty_portfolio():
    """Test calculation with empty portfolio values."""
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0])  # Only initial value
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['total_return_pct'] == 0.0, "Should handle single portfolio value"


def test_calculate_metrics_with_trade_log():
    """Test that function accepts trade log but focuses on portfolio values for return calculation."""
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1100.0])
    trade_log = [{'buy_price': 100, 'sell_price': 110, 'shares': 10, 'profit': 100}]
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert: Should calculate return based on portfolio values, not trade log
    assert result['total_return_pct'] == 10.0, "Should calculate return from portfolio values"


def test_calculate_metrics_negative_initial_capital():
    """Test error handling for invalid initial capital."""
    with pytest.raises((ValueError, ZeroDivisionError)):
        metrics.calculate_metrics([], pd.Series([1000.0, 1200.0]), 0.0)


def test_calculate_metrics_with_risk_free_rate():
    """Test that function accepts risk_free_rate parameter (for future use)."""
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1200.0])
    trade_log = []
    
    # Act: Should not raise error with risk_free_rate parameter
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital, risk_free_rate=0.05)
    
    # Assert: For Task 23, risk_free_rate not used yet but should be accepted
    assert result['total_return_pct'] == 20.0, "Should still calculate basic return correctly"


def test_print_metrics_console_output(capsys):
    """Test that print_metrics produces expected console output."""
    # Arrange
    test_metrics = {
        'total_return_pct': 15.75,
        'annualized_return_pct': 8.23
    }
    
    # Act
    metrics.print_metrics(test_metrics)
    
    # Assert
    captured = capsys.readouterr()
    assert "=== Performance Metrics ===" in captured.out
    assert "Total Return: 15.75%" in captured.out
    assert "Annualized Return: 8.23%" in captured.out


def test_print_metrics_partial_data(capsys):
    """Test print_metrics with partial metric data."""
    # Arrange: Only total return
    test_metrics = {'total_return_pct': 10.0}
    
    # Act
    metrics.print_metrics(test_metrics)
    
    # Assert: Should print available metrics without error
    captured = capsys.readouterr()
    assert "Total Return: 10.00%" in captured.out
    assert "Annualized Return" not in captured.out  # Should not print missing metrics


# =============================================================================
# TDD Tests for Task 24: Drawdown and Trade Metrics
# =============================================================================

def test_calculate_metrics_max_drawdown_simple():
    """Test max drawdown calculation with simple portfolio decline."""
    # Arrange: Portfolio that goes 1000 -> 1200 (peak) -> 900 (trough) -> 1100
    # Max drawdown should be (900 - 1200) / 1200 = -25%
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1200.0, 900.0, 1100.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert 'max_drawdown_pct' in result, "Result should contain max_drawdown_pct"
    expected_drawdown = -25.0  # -25% from peak 1200 to trough 900
    assert abs(result['max_drawdown_pct'] - expected_drawdown) < 0.1, f"Should calculate {expected_drawdown}% max drawdown"


def test_calculate_metrics_max_drawdown_no_drawdown():
    """Test max drawdown when portfolio only increases (no drawdown)."""
    # Arrange: Portfolio that only goes up: 1000 -> 1100 -> 1200 -> 1300
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1100.0, 1200.0, 1300.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['max_drawdown_pct'] == 0.0, "Should return 0% drawdown for only increasing portfolio"


def test_calculate_metrics_max_drawdown_single_value():
    """Test max drawdown with single portfolio value."""
    # Arrange: Portfolio with only initial value
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['max_drawdown_pct'] == 0.0, "Should return 0% drawdown for single value"


def test_calculate_metrics_trade_count_zero_trades():
    """Test trade count with no completed trades."""
    # Arrange: No trades completed
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1100.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert 'trade_count' in result, "Result should contain trade_count"
    assert result['trade_count'] == 0, "Should return 0 trade count for empty trade log"


def test_calculate_metrics_trade_count_multiple_trades():
    """Test trade count with multiple completed trades."""
    # Arrange: Three completed trades
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1100.0, 1200.0])
    trade_log = [
        {'buy_price': 100, 'sell_price': 110, 'shares': 10, 'profit': 100},
        {'buy_price': 110, 'sell_price': 120, 'shares': 9, 'profit': 90},
        {'buy_price': 120, 'sell_price': 115, 'shares': 8, 'profit': -40}
    ]
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['trade_count'] == 3, "Should return correct count of completed trades"


def test_calculate_metrics_win_rate_no_trades():
    """Test win rate calculation with no trades."""
    # Arrange: No trades completed
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1100.0])
    trade_log = []
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert 'win_rate_pct' in result, "Result should contain win_rate_pct"
    assert result['win_rate_pct'] == 0.0, "Should return 0% win rate for no trades"


def test_calculate_metrics_win_rate_all_winning_trades():
    """Test win rate calculation with all profitable trades."""
    # Arrange: Three winning trades
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1100.0, 1200.0, 1300.0])
    trade_log = [
        {'buy_price': 100, 'sell_price': 110, 'shares': 10, 'profit': 100},
        {'buy_price': 110, 'sell_price': 120, 'shares': 9, 'profit': 90},
        {'buy_price': 120, 'sell_price': 125, 'shares': 8, 'profit': 40}
    ]
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['win_rate_pct'] == 100.0, "Should return 100% win rate for all winning trades"


def test_calculate_metrics_win_rate_mixed_trades():
    """Test win rate calculation with mixed profitable and losing trades."""
    # Arrange: 2 winning trades, 1 losing trade = 66.67% win rate
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1100.0, 1200.0, 1150.0])
    trade_log = [
        {'buy_price': 100, 'sell_price': 110, 'shares': 10, 'profit': 100},  # Win
        {'buy_price': 110, 'sell_price': 120, 'shares': 9, 'profit': 90},   # Win
        {'buy_price': 120, 'sell_price': 115, 'shares': 8, 'profit': -40}   # Loss
    ]
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    expected_win_rate = (2 / 3) * 100.0  # 66.67%
    assert abs(result['win_rate_pct'] - expected_win_rate) < 0.1, "Should calculate correct win rate for mixed trades"


def test_calculate_metrics_win_rate_all_losing_trades():
    """Test win rate calculation with all losing trades."""
    # Arrange: Three losing trades
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 950.0, 900.0, 850.0])
    trade_log = [
        {'buy_price': 100, 'sell_price': 95, 'shares': 10, 'profit': -50},
        {'buy_price': 95, 'sell_price': 90, 'shares': 10, 'profit': -50},
        {'buy_price': 90, 'sell_price': 85, 'shares': 10, 'profit': -50}
    ]
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert result['win_rate_pct'] == 0.0, "Should return 0% win rate for all losing trades"


def test_calculate_metrics_win_rate_zero_profit_trades():
    """Test win rate calculation with break-even trades."""
    # Arrange: Mix of winning, losing, and break-even trades
    initial_capital = 1000.0
    portfolio_values = pd.Series([1000.0, 1000.0, 1050.0, 1050.0])
    trade_log = [
        {'buy_price': 100, 'sell_price': 100, 'shares': 10, 'profit': 0},    # Break-even (not a win)
        {'buy_price': 100, 'sell_price': 105, 'shares': 10, 'profit': 50},   # Win
        {'buy_price': 105, 'sell_price': 105, 'shares': 10, 'profit': 0}     # Break-even (not a win)
    ]
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    expected_win_rate = (1 / 3) * 100.0  # 33.33% (only 1 out of 3 is profitable)
    assert abs(result['win_rate_pct'] - expected_win_rate) < 0.1, "Should treat break-even trades as non-winning"


def test_print_metrics_with_task24_metrics(capsys):
    """Test print_metrics displays new Task 24 metrics properly."""
    # Arrange
    test_metrics = {
        'total_return_pct': 15.75,
        'annualized_return_pct': 8.23,
        'max_drawdown_pct': -12.45,
        'trade_count': 5,
        'win_rate_pct': 60.0
    }
    
    # Act
    metrics.print_metrics(test_metrics)
    
    # Assert
    captured = capsys.readouterr()
    assert "=== Performance Metrics ===" in captured.out
    assert "Total Return: 15.75%" in captured.out
    assert "Annualized Return: 8.23%" in captured.out
    assert "Max Drawdown: -12.45%" in captured.out
    assert "Number of Trades: 5" in captured.out
    assert "Win Rate: 60.00%" in captured.out


def test_print_metrics_partial_task24_data(capsys):
    """Test print_metrics with only some Task 24 metrics present."""
    # Arrange: Only some new metrics present
    test_metrics = {
        'total_return_pct': 10.0,
        'trade_count': 3,
        'win_rate_pct': 66.67
    }
    
    # Act
    metrics.print_metrics(test_metrics)
    
    # Assert
    captured = capsys.readouterr()
    assert "Total Return: 10.00%" in captured.out
    assert "Number of Trades: 3" in captured.out
    assert "Win Rate: 66.67%" in captured.out
    assert "Max Drawdown" not in captured.out  # Should not print missing metrics
    assert "Annualized Return" not in captured.out


# Task 25: Add risk/reward metrics tests

def test_calculate_sharpe_ratio_positive_returns():
    """Test Sharpe ratio calculation with positive returns."""
    # Arrange: Create series of daily returns
    returns = pd.Series([0.01, 0.02, -0.005, 0.015, 0.008])  # 1%, 2%, -0.5%, etc.
    risk_free_rate = 0.0
    
    # Act
    sharpe = metrics._calculate_sharpe_ratio(returns, risk_free_rate)
    
    # Assert
    # For this set of returns, with mean=0.0096, std=0.0094, annualized sharpe ≈ 1.61
    expected_sharpe = (returns.mean() / returns.std()) * np.sqrt(252)  # Annualized 
    assert abs(sharpe - expected_sharpe) < 0.01, "Should calculate correct positive Sharpe ratio"


def test_calculate_sharpe_ratio_negative_returns():
    """Test Sharpe ratio calculation with negative returns."""
    # Arrange: Create series of negative daily returns
    returns = pd.Series([-0.01, -0.02, -0.005, -0.015, -0.008])
    risk_free_rate = 0.0
    
    # Act
    sharpe = metrics._calculate_sharpe_ratio(returns, risk_free_rate)
    
    # Assert
    expected_sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    assert abs(sharpe - expected_sharpe) < 0.01, "Should calculate correct negative Sharpe ratio"


def test_calculate_sharpe_ratio_with_risk_free_rate():
    """Test Sharpe ratio calculation with non-zero risk-free rate."""
    # Arrange: Returns and 2% risk-free rate
    returns = pd.Series([0.03, 0.02, 0.04, 0.01, 0.02])
    risk_free_rate = 0.0002  # Approx 5% annualized (0.05/252)
    
    # Act
    sharpe = metrics._calculate_sharpe_ratio(returns, risk_free_rate)
    
    # Assert
    excess_returns = returns - risk_free_rate
    expected_sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
    assert abs(sharpe - expected_sharpe) < 0.01, "Should calculate Sharpe ratio with risk-free rate"


def test_calculate_sharpe_ratio_empty_returns():
    """Test Sharpe ratio calculation with empty returns."""
    # Arrange
    returns = pd.Series([])
    risk_free_rate = 0.0
    
    # Act
    sharpe = metrics._calculate_sharpe_ratio(returns, risk_free_rate)
    
    # Assert
    assert sharpe == 0.0, "Should return 0.0 for empty returns"


def test_calculate_profit_factor_all_winning():
    """Test profit factor calculation with all winning trades."""
    # Arrange
    trade_log = [
        {'profit': 100},
        {'profit': 50},
        {'profit': 75}
    ]
    
    # Act
    profit_factor = metrics._calculate_profit_factor(trade_log)
    
    # Assert
    assert profit_factor == float('inf'), "Profit factor should be infinity with no losing trades"


def test_calculate_profit_factor_all_losing():
    """Test profit factor calculation with all losing trades."""
    # Arrange
    trade_log = [
        {'profit': -100},
        {'profit': -50},
        {'profit': -75}
    ]
    
    # Act
    profit_factor = metrics._calculate_profit_factor(trade_log)
    
    # Assert
    assert profit_factor == 0.0, "Profit factor should be 0 with no winning trades"


def test_calculate_profit_factor_mixed():
    """Test profit factor calculation with mixed trades."""
    # Arrange
    trade_log = [
        {'profit': 100},   # Win
        {'profit': -50},   # Loss
        {'profit': 75},    # Win
        {'profit': -25}    # Loss
    ]
    
    # Act
    profit_factor = metrics._calculate_profit_factor(trade_log)
    
    # Assert
    # Total profit: 175, Total loss: 75, Profit factor: 175/75 = 2.33...
    assert abs(profit_factor - (175/75)) < 0.01, "Should calculate correct profit factor"


def test_calculate_profit_factor_with_breakeven():
    """Test profit factor calculation with break-even trades."""
    # Arrange
    trade_log = [
        {'profit': 100},  # Win
        {'profit': 0},    # Break-even
        {'profit': -50}   # Loss
    ]
    
    # Act
    profit_factor = metrics._calculate_profit_factor(trade_log)
    
    # Assert
    # Total profit: 100, Total loss: 50, Profit factor: 100/50 = 2.0
    assert profit_factor == 2.0, "Should calculate correct profit factor with break-even trades"


def test_calculate_profit_factor_empty():
    """Test profit factor calculation with empty trade log."""
    # Arrange
    trade_log = []
    
    # Act
    profit_factor = metrics._calculate_profit_factor(trade_log)
    
    # Assert
    assert profit_factor == 0.0, "Should return 0.0 for empty trade log"


def test_calculate_avg_win_pct_basic():
    """Test average win percentage calculation."""
    # Arrange
    trade_log = [
        {'profit': 100, 'buy_price': 1000, 'shares': 10},  # 10% win
        {'profit': 300, 'buy_price': 1500, 'shares': 10}   # 20% win
    ]
    
    # Act
    avg_win = metrics._calculate_avg_win_pct(trade_log)
      # Assert
    assert abs(avg_win - 1.5) < 0.01, "Should calculate average win percentage correctly (ROI per trade)"


def test_calculate_avg_win_pct_no_winners():
    """Test average win percentage with no winning trades."""
    # Arrange
    trade_log = [
        {'profit': -100, 'buy_price': 1000, 'shares': 10},
        {'profit': -50, 'buy_price': 500, 'shares': 10}
    ]
    
    # Act
    avg_win = metrics._calculate_avg_win_pct(trade_log)
    
    # Assert
    assert avg_win == 0.0, "Should return 0.0 when there are no winning trades"


def test_calculate_avg_win_pct_empty():
    """Test average win percentage with empty trade log."""
    # Arrange
    trade_log = []
    
    # Act
    avg_win = metrics._calculate_avg_win_pct(trade_log)
    
    # Assert
    assert avg_win == 0.0, "Should return 0.0 for empty trade log"


def test_calculate_avg_loss_pct_basic():
    """Test average loss percentage calculation."""
    # Arrange
    trade_log = [
        {'profit': -100, 'buy_price': 1000, 'shares': 10},  # 10% loss
        {'profit': -300, 'buy_price': 1500, 'shares': 10}   # 20% loss
    ]
    
    # Act
    avg_loss = metrics._calculate_avg_loss_pct(trade_log)
      # Assert
    assert abs(avg_loss - (-1.5)) < 0.01, "Should calculate average loss percentage correctly (ROI per trade)"


def test_calculate_avg_loss_pct_no_losers():
    """Test average loss percentage with no losing trades."""
    # Arrange
    trade_log = [
        {'profit': 100, 'buy_price': 1000, 'shares': 10},
        {'profit': 50, 'buy_price': 500, 'shares': 10}
    ]
    
    # Act
    avg_loss = metrics._calculate_avg_loss_pct(trade_log)
    
    # Assert
    assert avg_loss == 0.0, "Should return 0.0 when there are no losing trades"


def test_calculate_avg_loss_pct_empty():
    """Test average loss percentage with empty trade log."""
    # Arrange
    trade_log = []
    
    # Act
    avg_loss = metrics._calculate_avg_loss_pct(trade_log)
    
    # Assert
    assert avg_loss == 0.0, "Should return 0.0 for empty trade log"


def test_metrics_integration_risk_reward():
    """Test all risk/reward metrics integrated in calculate_metrics output."""
    # Arrange
    initial_capital = 1000.0
    start_date = pd.Timestamp('2022-01-01')
    dates = pd.date_range(start_date, periods=5)
    portfolio_values = pd.Series([1000.0, 1050.0, 1030.0, 1080.0, 1100.0], index=dates)
    
    # Mix of winning and losing trades
    trade_log = [
        {'buy_price': 100, 'sell_price': 110, 'shares': 10, 'profit': 100},
        {'buy_price': 110, 'sell_price': 100, 'shares': 10, 'profit': -100},
        {'buy_price': 100, 'sell_price': 120, 'shares': 5, 'profit': 100}
    ]
    
    # Act
    result = metrics.calculate_metrics(trade_log, portfolio_values, initial_capital)
    
    # Assert
    assert 'sharpe_ratio' in result, "Result should include Sharpe ratio"
    assert 'profit_factor' in result, "Result should include profit factor"
    assert 'avg_win_pct' in result, "Result should include average win percentage"
    assert 'avg_loss_pct' in result, "Result should include average loss percentage"
    
    # Basic checks on values
    assert result['profit_factor'] == 2.0, "Profit factor should be 2.0"
    assert result['avg_win_pct'] > 0, "Average win percentage should be positive"
    assert result['avg_loss_pct'] < 0, "Average loss percentage should be negative"


def test_print_metrics_with_task25_metrics(capsys):
    """Test print_metrics displays Task 25 risk/reward metrics."""
    # Arrange
    test_metrics = {
        'total_return_pct': 15.75,
        'annualized_return_pct': 8.23,
        'max_drawdown_pct': -12.45,
        'trade_count': 5,
        'win_rate_pct': 60.0,
        'sharpe_ratio': 1.25,
        'profit_factor': 2.5,
        'avg_win_pct': 1.5,
        'avg_loss_pct': -1.5
    }
    
    # Act
    metrics.print_metrics(test_metrics)
    
    # Assert
    captured = capsys.readouterr()
    assert "Sharpe Ratio: 1.25" in captured.out
    assert "Profit Factor: 2.50" in captured.out
    assert "Average Win: 1.50%" in captured.out
    assert "Average Loss: -1.50%" in captured.out
