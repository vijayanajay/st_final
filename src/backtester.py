"""
backtester.py

Framework for simulating trades based on strategy signals.
Implements the run_backtest function as specified in the design document.
"""
import pandas as pd
from typing import List, Dict, Tuple, NamedTuple, Optional
import logging

# Constants for better code readability
HOLD_SIGNAL = 0
BUY_SIGNAL = 1
SELL_SIGNAL = -1
FULL_PERCENT = 100.0

class PortfolioData(NamedTuple):
    """Enhanced portfolio data structure with composition and analytics."""
    portfolio_values: pd.Series
    cash_values: pd.Series
    equity_values: pd.Series
    cash_pct: pd.Series
    equity_pct: pd.Series
    period_returns: pd.Series
    cumulative_returns: pd.Series
    running_drawdown: pd.Series
    peak_values: pd.Series


def _calculate_portfolio_metrics(
    cash: float,
    shares: float,
    price: float,
    initial_capital: float,
    previous_portfolio_value: float,
    peak_value: float
) -> Tuple[float, float, float, float, float, float, float]:
    """
    Calculate portfolio metrics for a given state.
    
    Returns:
        tuple: (portfolio_value, cash_pct, equity_pct, period_return, 
                cumulative_return, drawdown, new_peak_value)
    """
    cash_value = cash
    equity_value = shares * price
    portfolio_value = cash_value + equity_value
    
    # Calculate percentages
    if portfolio_value > 0:
        cash_percentage = (cash_value / portfolio_value) * FULL_PERCENT
        equity_percentage = (equity_value / portfolio_value) * FULL_PERCENT
    else:
        cash_percentage = FULL_PERCENT
        equity_percentage = 0.0
    
    # Calculate returns
    if previous_portfolio_value > 0:
        period_return = ((portfolio_value - previous_portfolio_value) / previous_portfolio_value) * FULL_PERCENT
    else:
        period_return = 0.0
    
    cumulative_return = ((portfolio_value - initial_capital) / initial_capital) * FULL_PERCENT
    
    # Calculate drawdown and update peak
    new_peak_value = max(peak_value, portfolio_value)
    if new_peak_value > 0:
        drawdown = ((portfolio_value - new_peak_value) / new_peak_value) * FULL_PERCENT
    else:
        drawdown = 0.0
    
    return (portfolio_value, cash_percentage, equity_percentage, 
            period_return, cumulative_return, drawdown, new_peak_value)


def _process_trading_signals(
    df_with_signals: pd.DataFrame,
    initial_capital: float,
    signal_col: str,
    price_col: str,
    enhanced_tracking: bool = False
) -> Tuple[List[Dict], pd.Series, Optional[PortfolioData]]:
    """
    Core trading logic shared between basic and enhanced backtesting.
    
    Args:
        df_with_signals: DataFrame with signals and prices
        initial_capital: Starting capital
        signal_col: Name of signal column
        price_col: Name of price column
        enhanced_tracking: Whether to track detailed portfolio metrics
        
    Returns:
        tuple: (trade_log, portfolio_values, portfolio_data)
               portfolio_data is None for basic tracking
    """
    logger = logging.getLogger(__name__)
    
    # Initialize simulation state
    cash = initial_capital
    shares = 0.0
    trade_log = []
    position_open = False
    buy_price = 0.0
    
    # Initialize tracking arrays
    portfolio_values = []
    if enhanced_tracking:
        cash_values = []
        equity_values = []
        cash_pct = []
        equity_pct = []
        period_returns = []
        cumulative_returns = []
        running_drawdown = []
        peak_values = []
        
        previous_portfolio_value = initial_capital
        peak_value = initial_capital
    
    # Process each row of data
    for index, row in df_with_signals.iterrows():
        signal = row[signal_col]
        price = row[price_col]
        
        # Process signals
        if signal == BUY_SIGNAL and not position_open:  # Buy signal
            shares = cash / price
            buy_price = price
            cash = 0.0
            position_open = True
            logger.debug(f"BUY: {shares:.4f} shares at {price}")
        
        elif signal == SELL_SIGNAL and position_open:  # Sell signal
            cash = shares * price
            profit = (price - buy_price) * shares
            trade_log.append({
                'buy_price': buy_price,
                'sell_price': price,
                'shares': shares,
                'profit': profit
            })
            shares = 0.0
            position_open = False
            logger.debug(f"SELL: shares at {price}, profit: {profit}")
        
        # Calculate portfolio value
        portfolio_value = cash + (shares * price)
        portfolio_values.append(portfolio_value)
        
        # Enhanced tracking if requested
        if enhanced_tracking:
            metrics = _calculate_portfolio_metrics(
                cash, shares, price, initial_capital,
                previous_portfolio_value, peak_value
            )
            (calc_portfolio_value, cash_percentage, equity_percentage, 
             period_return, cumulative_return, drawdown, new_peak_value) = metrics
            
            cash_values.append(cash)
            equity_values.append(shares * price)
            cash_pct.append(cash_percentage)
            equity_pct.append(equity_percentage)
            period_returns.append(period_return)
            cumulative_returns.append(cumulative_return)
            running_drawdown.append(drawdown)
            peak_values.append(new_peak_value)
            
            previous_portfolio_value = portfolio_value
            peak_value = new_peak_value
    
    # Create return values
    portfolio_series = pd.Series(portfolio_values, index=df_with_signals.index)
    
    if enhanced_tracking:
        portfolio_data = PortfolioData(
            portfolio_values=portfolio_series,
            cash_values=pd.Series(cash_values, index=df_with_signals.index),
            equity_values=pd.Series(equity_values, index=df_with_signals.index),
            cash_pct=pd.Series(cash_pct, index=df_with_signals.index),
            equity_pct=pd.Series(equity_pct, index=df_with_signals.index),
            period_returns=pd.Series(period_returns, index=df_with_signals.index),
            cumulative_returns=pd.Series(cumulative_returns, index=df_with_signals.index),
            running_drawdown=pd.Series(running_drawdown, index=df_with_signals.index),
            peak_values=pd.Series(peak_values, index=df_with_signals.index)
        )
        return trade_log, portfolio_series, portfolio_data
    else:
        return trade_log, portfolio_series, None


def run_backtest(
    df_with_signals: pd.DataFrame,
    initial_capital: float,
    signal_col: str = 'Signal',
    price_col: str = 'Close'
) -> Tuple[List[Dict], pd.Series]:
    """
    Simulate trading based on signals in the DataFrame.

    Args:
        df_with_signals (pd.DataFrame): DataFrame containing at least signal and price columns.
        initial_capital (float): Starting cash for the simulation.
        signal_col (str): Name of the column with trading signals (default 'Signal').
        price_col (str): Name of the column with price data (default 'Close').

    Returns:
        tuple: (trade_log, portfolio_values)
            trade_log (list of dict): List of trade events (empty for skeleton).
            portfolio_values (pd.Series): Series of portfolio values (empty for skeleton).

    Raises:
        ValueError: If required columns are missing.
    """
    logger = logging.getLogger(__name__)
    
    # Validate inputs
    if signal_col not in df_with_signals.columns:
        raise ValueError(f"Signal column '{signal_col}' not found in DataFrame.")
    if price_col not in df_with_signals.columns:
        raise ValueError(f"Price column '{price_col}' not found in DataFrame.")
    
    logger.info(f"run_backtest called with initial_capital={initial_capital}")
    
    # Use shared trading logic
    trade_log, portfolio_values, _ = _process_trading_signals(
        df_with_signals, initial_capital, signal_col, price_col, enhanced_tracking=False
    )
    
    return trade_log, portfolio_values


def run_backtest_enhanced(
    df_with_signals: pd.DataFrame,
    initial_capital: float,
    signal_col: str = 'Signal',
    price_col: str = 'Close'
) -> Tuple[List[Dict], PortfolioData]:
    """
    Enhanced backtesting with detailed portfolio composition and analytics.

    Args:
        df_with_signals (pd.DataFrame): DataFrame containing at least signal and price columns.
        initial_capital (float): Starting cash for the simulation.
        signal_col (str): Name of the column with trading signals (default 'Signal').
        price_col (str): Name of the column with price data (default 'Close').

    Returns:
        tuple: (trade_log, portfolio_data)
            trade_log (list of dict): List of trade events.
            portfolio_data (PortfolioData): Enhanced portfolio tracking data.

    Raises:
        ValueError: If required columns are missing.
    """
    logger = logging.getLogger(__name__)
    
    # Validate inputs
    if signal_col not in df_with_signals.columns:
        raise ValueError(f"Signal column '{signal_col}' not found in DataFrame.")
    if price_col not in df_with_signals.columns:
        raise ValueError(f"Price column '{price_col}' not found in DataFrame.")
    
    logger.info(f"run_backtest_enhanced called with initial_capital={initial_capital}")
    
    # Use shared trading logic with enhanced tracking
    trade_log, _, portfolio_data = _process_trading_signals(
        df_with_signals, initial_capital, signal_col, price_col, enhanced_tracking=True
    )
    
    return trade_log, portfolio_data
