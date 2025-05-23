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


# TDD Phase 1: Basic Trade Logic Tests

def test_run_backtest_single_buy_signal():
    """Test that a single buy signal results in position entry."""
    # Arrange: DataFrame with one buy signal at index 1
    df = pd.DataFrame({
        'Signal': [0, 1, 0],
        'Close': [100, 110, 120]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: Should have an open position but no completed trades yet
    # Portfolio value should reflect the position at current price
    assert len(portfolio_values) == 3, "Should have portfolio values for each row"
    assert portfolio_values.iloc[0] == initial_capital, "Initial portfolio value should equal initial capital"
    
    # After buy signal, portfolio should reflect shares held at current price
    # Assuming we buy as many shares as possible: shares = cash / price
    expected_shares = initial_capital / 110  # Buy at price 110
    expected_portfolio_value_after_buy = expected_shares * 120  # Value at price 120
    
    # Portfolio value at the end should reflect the position
    assert abs(portfolio_values.iloc[2] - expected_portfolio_value_after_buy) < 0.01, \
        f"Portfolio value should reflect position value. Expected: {expected_portfolio_value_after_buy}, Got: {portfolio_values.iloc[2]}"
    
    # No completed trades yet since we only have a buy signal
    assert len(trade_log) == 0, "Should have no completed trades with only a buy signal"


def test_run_backtest_complete_trade_cycle():
    """Test a complete buy-sell cycle generates correct trade log and portfolio values."""
    # Arrange: Buy signal followed by sell signal
    df = pd.DataFrame({
        'Signal': [0, 1, 0, -1, 0],
        'Close': [100, 110, 115, 120, 125]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
      # Assert: Should have one completed trade
    assert len(trade_log) == 1, "Should have exactly one completed trade"
    
    trade = trade_log[0]
    expected_shares = initial_capital / 110  # Bought at 110
    expected_profit = (120 - 110) * expected_shares  # Profit per share * shares
    
    assert abs(trade['shares'] - expected_shares) < 0.0001, "Trade should record correct number of shares"
    assert trade['sell_price'] == 120, "Trade should record correct sell price"
    assert abs(trade['profit'] - expected_profit) < 0.01, "Trade should calculate correct profit"
    
    # Portfolio values should track the position correctly
    assert len(portfolio_values) == 5, "Should have portfolio values for each row"
    assert portfolio_values.iloc[0] == initial_capital, "Initial portfolio value should equal initial capital"
    
    # After buy: portfolio = shares * current_price
    expected_portfolio_after_buy = expected_shares * 115  # Value at row 2 (price 115)
    assert abs(portfolio_values.iloc[2] - expected_portfolio_after_buy) < 0.01, \
        "Portfolio value should reflect position value during holding period"
    
    # After sell: portfolio = cash (no shares)
    expected_final_cash = expected_shares * 120  # Sold at 120
    assert abs(portfolio_values.iloc[3] - expected_final_cash) < 0.01, \
        "Portfolio value should equal cash after selling"
    assert abs(portfolio_values.iloc[4] - expected_final_cash) < 0.01, \
        "Portfolio value should remain as cash when no position"


def test_run_backtest_hold_signals():
    """Test that hold signals (0) don't trigger any trades."""
    # Arrange: Only hold signals
    df = pd.DataFrame({
        'Signal': [0, 0, 0, 0],
        'Close': [100, 110, 115, 120]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: No trades should occur
    assert len(trade_log) == 0, "No trades should occur with only hold signals"
    
    # Portfolio value should remain constant (all cash, no position)
    for value in portfolio_values:
        assert value == initial_capital, "Portfolio value should remain as initial capital with no trades"


def test_run_backtest_ignore_redundant_buy_signals():
    """Test that redundant buy signals are ignored when already in position."""
    # Arrange: Multiple buy signals without sell
    df = pd.DataFrame({
        'Signal': [0, 1, 1, 1, 0],  # Multiple buy signals
        'Close': [100, 110, 115, 120, 125]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: Should only buy once (first signal), ignore subsequent buy signals
    assert len(trade_log) == 0, "No completed trades with only buy signals"
    
    # Should have bought shares at first signal (110) and held them
    expected_shares = initial_capital / 110
    
    # Portfolio values should reflect the same position throughout
    expected_value_at_115 = expected_shares * 115
    expected_value_at_120 = expected_shares * 120
    expected_value_at_125 = expected_shares * 125
    
    assert abs(portfolio_values.iloc[2] - expected_value_at_115) < 0.01, \
        "Portfolio value should reflect held position at price 115"
    assert abs(portfolio_values.iloc[3] - expected_value_at_120) < 0.01, \
        "Portfolio value should reflect held position at price 120"
    assert abs(portfolio_values.iloc[4] - expected_value_at_125) < 0.01, \
        "Portfolio value should reflect held position at price 125"


def test_run_backtest_ignore_sell_without_position():
    """Test that sell signals are ignored when no position is held."""
    # Arrange: Sell signals without prior buy
    df = pd.DataFrame({
        'Signal': [0, -1, -1, 0],  # Sell signals without position
        'Close': [100, 110, 115, 120]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: No trades should occur
    assert len(trade_log) == 0, "No trades should occur when selling without position"
    
    # Portfolio value should remain constant (all cash, no position)
    for value in portfolio_values:
        assert value == initial_capital, "Portfolio value should remain as initial capital when no position to sell"


def test_run_backtest_multiple_trades():
    """Test multiple complete trade cycles."""
    # Arrange: Two complete buy-sell cycles
    df = pd.DataFrame({
        'Signal': [0, 1, 0, -1, 0, 1, 0, -1, 0],
        'Close': [100, 110, 115, 120, 125, 130, 135, 140, 145]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: Should have two completed trades
    assert len(trade_log) == 2, "Should have exactly two completed trades"
      # First trade: buy at 110, sell at 120
    trade1 = trade_log[0]
    expected_shares1 = initial_capital / 110
    expected_profit1 = (120 - 110) * expected_shares1  # Profit per share * shares
    
    assert abs(trade1['shares'] - expected_shares1) < 0.0001, "First trade should record correct shares"
    assert trade1['sell_price'] == 120, "First trade should record correct sell price"
    assert abs(trade1['profit'] - expected_profit1) < 0.01, "First trade should calculate correct profit"
    
    # Second trade: buy at 130, sell at 140 (with cash from first trade)
    trade2 = trade_log[1]
    cash_after_first_trade = expected_shares1 * 120
    expected_shares2 = cash_after_first_trade / 130
    expected_profit2 = (140 - 130) * expected_shares2  # Profit per share * shares
    
    assert abs(trade2['shares'] - expected_shares2) < 0.0001, "Second trade should record correct shares"
    assert trade2['sell_price'] == 140, "Second trade should record correct sell price"
    assert abs(trade2['profit'] - expected_profit2) < 0.01, "Second trade should calculate correct profit"
    
    # Final portfolio value should equal cash after second trade
    final_cash = expected_shares2 * 140
    assert abs(portfolio_values.iloc[-1] - final_cash) < 0.01, "Final portfolio value should equal final cash"


def test_run_backtest_open_position_at_end():
    """Test handling of open position at the end of the simulation."""
    # Arrange: Buy signal but no sell signal (position remains open)
    df = pd.DataFrame({
        'Signal': [0, 1, 0, 0],
        'Close': [100, 110, 115, 120]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: No completed trades (position still open)
    assert len(trade_log) == 0, "Should have no completed trades with open position"
    
    # Portfolio value should reflect the held position at final price
    expected_shares = initial_capital / 110  # Bought at 110
    expected_final_value = expected_shares * 120  # Value at final price 120
    
    assert abs(portfolio_values.iloc[-1] - expected_final_value) < 0.01, \
        "Final portfolio value should reflect open position value"


def test_run_backtest_trade_log_structure():
    """Test that trade log includes buy_price for complete profit calculation."""
    # Arrange: Simple buy-sell cycle
    df = pd.DataFrame({
        'Signal': [0, 1, -1],
        'Close': [100, 110, 120]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: Trade log should include buy_price
    assert len(trade_log) == 1, "Should have one completed trade"
    
    trade = trade_log[0]
    assert 'buy_price' in trade, "Trade log should include buy_price"
    assert 'sell_price' in trade, "Trade log should include sell_price"
    assert 'shares' in trade, "Trade log should include shares"
    assert 'profit' in trade, "Trade log should include profit"
    
    assert trade['buy_price'] == 110, "Should record correct buy price"
    assert trade['sell_price'] == 120, "Should record correct sell price"
    
    # Verify profit calculation: (sell_price - buy_price) * shares
    expected_shares = initial_capital / 110
    expected_profit = (120 - 110) * expected_shares
    assert abs(trade['profit'] - expected_profit) < 0.01, "Profit should be calculated correctly"


def test_run_backtest_empty_dataframe():
    """Test handling of empty DataFrame."""
    # Arrange: Empty DataFrame
    df = pd.DataFrame({'Signal': [], 'Close': []})
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: No trades and empty portfolio series
    assert len(trade_log) == 0, "Should have no trades with empty DataFrame"
    assert len(portfolio_values) == 0, "Should have empty portfolio values with empty DataFrame"


def test_run_backtest_custom_column_names():
    """Test backtester with custom signal and price column names."""
    # Arrange: DataFrame with custom column names
    df = pd.DataFrame({
        'custom_signal': [0, 1, 0, -1, 0],
        'custom_price': [100, 110, 115, 120, 125]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_values = backtester.run_backtest(
        df, initial_capital, 
        signal_col='custom_signal', 
        price_col='custom_price'
    )
    
    # Assert: Should complete one trade successfully
    assert len(trade_log) == 1, "Should have one completed trade with custom columns"
    
    trade = trade_log[0]
    assert trade['buy_price'] == 110, "Should record correct buy price"
    assert trade['sell_price'] == 120, "Should record correct sell price"
    
    expected_shares = initial_capital / 110
    expected_profit = (120 - 110) * expected_shares
    assert abs(trade['profit'] - expected_profit) < 0.01, "Should calculate correct profit"


# TDD Phase 1: Enhanced Portfolio Tracking Tests

def test_portfolio_composition_tracking():
    """Test that portfolio tracks cash vs equity composition over time."""
    # Arrange: Simple buy-hold-sell cycle
    df = pd.DataFrame({
        'Signal': [0, 1, 0, 0, -1],
        'Close': [100, 110, 115, 120, 125]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_data = backtester.run_backtest_enhanced(df, initial_capital)
    
    # Assert: Should have portfolio composition data
    assert hasattr(portfolio_data, 'cash_values'), "Should track cash values over time"
    assert hasattr(portfolio_data, 'equity_values'), "Should track equity values over time"
    assert hasattr(portfolio_data, 'cash_pct'), "Should track cash percentage over time"
    assert hasattr(portfolio_data, 'equity_pct'), "Should track equity percentage over time"
    
    # Initial state: 100% cash, 0% equity
    assert portfolio_data.cash_pct.iloc[0] == 100.0, "Should start with 100% cash"
    assert portfolio_data.equity_pct.iloc[0] == 0.0, "Should start with 0% equity"
      # After buy: should be 0% cash, 100% equity
    assert portfolio_data.cash_pct.iloc[1] == 0.0, "Should have exactly 0.0% cash after buying"
    assert portfolio_data.equity_pct.iloc[1] == 100.0, "Should have exactly 100.0% equity after buying"
    
    # After sell: should be 100% cash again
    assert portfolio_data.cash_pct.iloc[4] == 100.0, "Should be 100% cash after selling"
    assert portfolio_data.equity_pct.iloc[4] == 0.0, "Should be 0% equity after selling"


def test_portfolio_returns_calculation():
    """Test that portfolio calculates period-over-period returns."""
    # Arrange: Simple scenario with price changes
    df = pd.DataFrame({
        'Signal': [0, 1, 0, -1],
        'Close': [100, 110, 120, 130]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_data = backtester.run_backtest_enhanced(df, initial_capital)
    
    # Assert: Should have return calculations
    assert hasattr(portfolio_data, 'period_returns'), "Should calculate period returns"
    assert hasattr(portfolio_data, 'cumulative_returns'), "Should calculate cumulative returns"
    
    # First period should have 0 return (no position change)
    assert portfolio_data.period_returns.iloc[0] == 0.0, "First period should have 0 return"
    
    # Should have positive return when position gains value
    expected_return_pct = ((120 - 110) / 110) * 100  # ~9.09%
    assert abs(portfolio_data.period_returns.iloc[2] - expected_return_pct) < 0.1, "Should calculate correct period return"


def test_cumulative_returns_tracking():
    """Test cumulative return calculation over time."""
    # Arrange: Multi-period scenario
    df = pd.DataFrame({
        'Signal': [0, 1, 0, 0, 0],
        'Close': [100, 100, 110, 120, 130]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_data = backtester.run_backtest_enhanced(df, initial_capital)
    
    # Assert: Cumulative returns should compound
    assert portfolio_data.cumulative_returns.iloc[0] == 0.0, "Should start with 0% cumulative return"
    
    # After position gains 30%, cumulative return should be ~30%
    final_return = portfolio_data.cumulative_returns.iloc[-1]
    expected_final_return = 30.0  # 30% gain from 100 to 130
    assert abs(final_return - expected_final_return) < 1.0, "Should calculate correct cumulative return"


def test_portfolio_drawdown_calculation():
    """Test real-time drawdown calculation during simulation."""
    # Arrange: Scenario with peak and drawdown
    df = pd.DataFrame({
        'Signal': [0, 1, 0, 0, 0, 0],
        'Close': [100, 100, 120, 110, 105, 115]  # Peak at 120, drawdown to 105
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_data = backtester.run_backtest_enhanced(df, initial_capital)
    
    # Assert: Should track running drawdown
    assert hasattr(portfolio_data, 'running_drawdown'), "Should track running drawdown"
    assert hasattr(portfolio_data, 'peak_values'), "Should track peak portfolio values"
    
    # Should identify the correct maximum drawdown
    max_drawdown = portfolio_data.running_drawdown.min()
    expected_drawdown = -((120 - 105) / 120) * 100  # ~-12.5%
    assert abs(max_drawdown - expected_drawdown) < 1.0, "Should calculate correct maximum drawdown"


def test_enhanced_portfolio_data_structure():
    """Test that enhanced portfolio data includes all required fields."""
    # Arrange: Simple scenario
    df = pd.DataFrame({
        'Signal': [0, 1, -1],
        'Close': [100, 110, 120]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_data = backtester.run_backtest_enhanced(df, initial_capital)
    
    # Assert: Should have all required attributes
    required_attrs = [
        'portfolio_values', 'cash_values', 'equity_values',
        'cash_pct', 'equity_pct', 'period_returns', 'cumulative_returns',
        'running_drawdown', 'peak_values'
    ]
    
    for attr in required_attrs:
        assert hasattr(portfolio_data, attr), f"Portfolio data should have {attr} attribute"
        assert len(getattr(portfolio_data, attr)) == len(df), f"{attr} should have same length as input data"


def test_portfolio_data_integration():
    """Test that enhanced data integrates properly with existing trade log."""
    # Arrange: Complete trade cycle
    df = pd.DataFrame({
        'Signal': [0, 1, 0, -1, 0],
        'Close': [100, 110, 115, 120, 125]
    })
    initial_capital = 1000.0
    
    # Act
    trade_log, portfolio_data = backtester.run_backtest_enhanced(df, initial_capital)
    
    # Assert: Trade log should remain consistent
    assert len(trade_log) == 1, "Should have one completed trade"
    assert 'buy_price' in trade_log[0], "Trade log should maintain existing structure"
    
    # Portfolio data should be consistent with trade execution
    expected_shares = initial_capital / 110
    expected_final_cash = expected_shares * 120
    
    assert abs(portfolio_data.cash_values.iloc[-1] - expected_final_cash) < 0.01, "Cash values should match trade execution"
    assert portfolio_data.equity_values.iloc[-1] == 0.0, "Should have no equity after selling"


def test_backward_compatibility_with_run_backtest():
    """Test that original run_backtest function still works unchanged."""
    # Arrange: Same test case as existing tests
    df = pd.DataFrame({
        'Signal': [0, 1, 0, -1, 0],
        'Close': [100, 110, 115, 120, 125]
    })
    initial_capital = 1000.0
    
    # Act: Use original function
    trade_log, portfolio_values = backtester.run_backtest(df, initial_capital)
    
    # Assert: Should work exactly as before
    assert isinstance(trade_log, list), "Should return list for trade log"
    assert isinstance(portfolio_values, pd.Series), "Should return Series for portfolio values"
    assert len(trade_log) == 1, "Should have one completed trade"
    assert len(portfolio_values) == len(df), "Portfolio values should match DataFrame length"
