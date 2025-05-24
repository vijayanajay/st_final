"""
Tests for metrics.py module.
Task 23: Create metrics.py with basic return calculations (Total Return % and Annualized Return %)
"""
import pytest
import pandas as pd
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
