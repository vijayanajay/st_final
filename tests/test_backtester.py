import pytest
import pandas as pd
from src import backtester


def test_run_backtest_exists():
    assert hasattr(backtester, 'run_backtest'), "run_backtest function must exist in backtester.py"


def test_run_backtest_returns_types():
    df = pd.DataFrame({
        'Signal': [0, 1, 0],
        'Close': [100, 101, 102]
    })
    trade_log, portfolio_series = backtester.run_backtest(df, initial_capital=1000)
    assert isinstance(trade_log, list), "run_backtest must return a list as first output (trade log)"
    assert isinstance(portfolio_series, pd.Series), "run_backtest must return a pandas Series as second output (portfolio values)"


def test_run_backtest_missing_signal_col():
    df = pd.DataFrame({'Close': [100, 101, 102]})
    with pytest.raises(ValueError):
        backtester.run_backtest(df, initial_capital=1000)


def test_run_backtest_missing_price_col():
    df = pd.DataFrame({'Signal': [0, 1, 0]})
    with pytest.raises(ValueError):
        backtester.run_backtest(df, initial_capital=1000)


def test_run_backtest_docstring():
    assert backtester.run_backtest.__doc__ is not None and len(backtester.run_backtest.__doc__) > 10, "run_backtest should have a meaningful docstring"
