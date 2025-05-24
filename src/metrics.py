"""
metrics.py

Calculate performance metrics based on trade log and portfolio value series.
Task 23 focus: Basic return calculations (Total Return % and Annualized Return %)
Task 24: Add drawdown and trade metrics (Max Drawdown %, Trade Count, Win Rate %)
Task 25: Add risk/reward metrics (Sharpe Ratio, Profit Factor, Average Win/Loss %)
"""
import pandas as pd
import numpy as np
from typing import List, Dict


def _calculate_max_drawdown(portfolio_values: pd.Series) -> float:
    """
    Calculate maximum drawdown percentage from portfolio values.
    
    Args:
        portfolio_values: Series of portfolio values over time
        
    Returns:
        Maximum drawdown as negative percentage (e.g., -25.0 for 25% drawdown)
    """
    if len(portfolio_values) <= 1:
        return 0.0
    
    # Calculate running maximum (peak values)
    running_max = portfolio_values.cummax()
    
    # Calculate drawdown at each point as percentage
    drawdown = ((portfolio_values - running_max) / running_max) * 100.0
    
    # Return the minimum (most negative) drawdown
    max_drawdown = drawdown.min()
    
    # Return 0.0 if no drawdown occurred (all values were NaN or no decline)
    return max_drawdown if not pd.isna(max_drawdown) else 0.0


def _calculate_win_rate(trade_log: List[Dict]) -> float:
    """
    Calculate win rate percentage from trade log.
    
    Args:
        trade_log: List of completed trade dictionaries with 'profit' key
        
    Returns:
        Win rate as percentage (profitable trades / total trades * 100)
    """
    if len(trade_log) == 0:
        return 0.0
    
    # Count trades with positive profit
    winning_trades = sum(1 for trade in trade_log if trade['profit'] > 0)
    
    # Calculate win rate percentage
    win_rate = (winning_trades / len(trade_log)) * 100.0
    
    return win_rate


def _calculate_profit_factor(trade_log: List[Dict]) -> float:
    """
    Calculate profit factor (gross profits / gross losses).
    
    Args:
        trade_log: List of completed trade dictionaries with 'profit' key
        
    Returns:
        Profit factor (>1 is profitable, infinity for no losses, 0 for no wins or empty)
    """
    if len(trade_log) == 0:
        return 0.0
    
    total_profit = sum(trade['profit'] for trade in trade_log if trade['profit'] > 0)
    total_loss = sum(-trade['profit'] for trade in trade_log if trade['profit'] < 0)
    
    return float('inf') if total_loss == 0 and total_profit > 0 else (total_profit / total_loss if total_loss > 0 else 0.0)


def _calculate_avg_win_pct(trade_log: List[Dict]) -> float:
    """
    Calculate average win percentage from profitable trades.
    
    Args:
        trade_log: List of completed trade dictionaries with 'profit', 'buy_price', 'shares' keys
        
    Returns:
        Average win percentage (positive value), calculated as:
        (trade['profit'] / (trade['buy_price'] * trade['shares'])) * 100.0
        Handles division by zero gracefully (skips such trades).
    """
    if len(trade_log) == 0:
        return 0.0
    
    winning_trades = [trade for trade in trade_log if trade['profit'] > 0]
    
    if not winning_trades:
        return 0.0
    
    win_percentages = []
    for trade in winning_trades:
        cost_basis = trade['buy_price'] * trade['shares']
        if cost_basis == 0:
            continue  # skip to avoid division by zero
        win_pct = (trade['profit'] / cost_basis) * 100.0
        win_percentages.append(win_pct)
    
    return sum(win_percentages) / len(win_percentages) if win_percentages else 0.0


def _calculate_avg_loss_pct(trade_log: List[Dict]) -> float:
    """
    Calculate average loss percentage from losing trades.
    
    Args:
        trade_log: List of completed trade dictionaries with 'profit', 'buy_price', 'shares' keys
        
    Returns:
        Average loss percentage (negative value), calculated as:
        (trade['profit'] / (trade['buy_price'] * trade['shares'])) * 100.0
        Handles division by zero gracefully (skips such trades).
    """
    if len(trade_log) == 0:
        return 0.0
    
    losing_trades = [trade for trade in trade_log if trade['profit'] < 0]
    
    if not losing_trades:
        return 0.0
    
    loss_percentages = []
    for trade in losing_trades:
        cost_basis = trade['buy_price'] * trade['shares']
        if cost_basis == 0:
            continue  # skip to avoid division by zero
        loss_pct = (trade['profit'] / cost_basis) * 100.0
        loss_percentages.append(loss_pct)
    
    return sum(loss_percentages) / len(loss_percentages) if loss_percentages else 0.0


def _calculate_sharpe_ratio(portfolio_returns: pd.Series, risk_free_rate: float) -> float:
    """
    Calculate Sharpe Ratio from portfolio returns.
    
    Args:
        portfolio_returns: Series of portfolio returns
        risk_free_rate: Risk-free rate for calculations
        
    Returns:
        Sharpe Ratio (reward-to-variability ratio)
    """
    if len(portfolio_returns) == 0:
        return 0.0
    
    # Calculate excess returns over the risk-free rate
    excess_returns = portfolio_returns - risk_free_rate
    
    # Calculate and annualize the Sharpe Ratio (assuming daily returns, annualizing by sqrt(252))
    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
    
    return sharpe_ratio


def calculate_metrics(
    trade_log: List[Dict], 
    portfolio_values: pd.Series, 
    initial_capital: float, 
    risk_free_rate: float = 0.0
) -> Dict:
    """
    Calculate performance metrics from trade log and portfolio values.
    
    Args:
        trade_log: List of completed trade dictionaries
        portfolio_values: Series of portfolio values over time
        initial_capital: Starting capital amount
        risk_free_rate: Risk-free rate for calculations (default 0.0)
        
    Returns:
        Dictionary containing calculated metrics:
            'total_return_pct': Total return as percentage
            'annualized_return_pct': Annualized return as percentage
            'max_drawdown_pct': Maximum drawdown as percentage
            'trade_count': Total number of completed trades
            'win_rate_pct': Percentage of profitable trades
            'sharpe_ratio': Sharpe ratio (risk-adjusted return)
            'profit_factor': Ratio of gross profits to gross losses
            'avg_win_pct': Average percentage gain of winning trades
            'avg_loss_pct': Average percentage loss of losing trades
            
    Raises:
        ValueError: If initial_capital is <= 0 or portfolio_values is empty
    """
    # Input validation
    if initial_capital <= 0:
        raise ValueError("Initial capital must be positive")
    
    if len(portfolio_values) == 0:
        raise ValueError("Portfolio values cannot be empty")
    
    # For Task 23, implement basic return calculations
    final_value = portfolio_values.iloc[-1]
    
    # Calculate total return percentage
    total_return_pct = ((final_value - initial_capital) / initial_capital) * 100.0
    
    # Calculate annualized return
    if len(portfolio_values) >= 2 and hasattr(portfolio_values.index, 'to_pydatetime'):
        # Extract time period if index has datetime information
        start_date = portfolio_values.index[0]
        end_date = portfolio_values.index[-1]
        days = (end_date - start_date).days
        years = days / 365.25
        
        if years > 0:
            annualized_return_pct = (((final_value / initial_capital) ** (1.0 / years)) - 1.0) * 100.0
        else:
            annualized_return_pct = 0.0
    else:
        # If no time information available, set annualized return to 0
        annualized_return_pct = 0.0
    
    # Task 24: Calculate max drawdown from portfolio values
    max_drawdown_pct = _calculate_max_drawdown(portfolio_values)
    
    # Task 24: Calculate trade metrics from trade log
    trade_count = len(trade_log)
    win_rate_pct = _calculate_win_rate(trade_log)
    
    # Task 25: Calculate risk/reward metrics
    # Calculate daily portfolio returns (percentage)
    portfolio_returns = portfolio_values.pct_change().fillna(0)
    
    # Calculate Sharpe Ratio
    sharpe_ratio = _calculate_sharpe_ratio(portfolio_returns, risk_free_rate)
      # Calculate profit factor
    profit_factor = _calculate_profit_factor(trade_log)
    
    # Calculate average win and loss percentages
    avg_win_pct = _calculate_avg_win_pct(trade_log)
    avg_loss_pct = _calculate_avg_loss_pct(trade_log)
    
    return {
        'total_return_pct': total_return_pct,
        'annualized_return_pct': annualized_return_pct,
        'max_drawdown_pct': max_drawdown_pct,
        'trade_count': trade_count,
        'win_rate_pct': win_rate_pct,
        'sharpe_ratio': sharpe_ratio,
        'profit_factor': profit_factor,
        'avg_win_pct': avg_win_pct,
        'avg_loss_pct': avg_loss_pct
    }


def print_metrics(metrics_dict: Dict) -> None:
    """
    Print formatted metrics to console.
    
    Args:
        metrics_dict: Dictionary of metric names and values
    """
    print("=== Performance Metrics ===")
    
    if 'total_return_pct' in metrics_dict:
        print(f"Total Return: {metrics_dict['total_return_pct']:.2f}%")
    
    if 'annualized_return_pct' in metrics_dict:
        print(f"Annualized Return: {metrics_dict['annualized_return_pct']:.2f}%")
    
    if 'max_drawdown_pct' in metrics_dict:
        print(f"Max Drawdown: {metrics_dict['max_drawdown_pct']:.2f}%")
    
    if 'trade_count' in metrics_dict:
        print(f"Number of Trades: {metrics_dict['trade_count']}")
    
    if 'win_rate_pct' in metrics_dict:
        print(f"Win Rate: {metrics_dict['win_rate_pct']:.2f}%")
    
    if 'sharpe_ratio' in metrics_dict:
        print(f"Sharpe Ratio: {metrics_dict['sharpe_ratio']:.2f}")
    
    if 'profit_factor' in metrics_dict:
        print(f"Profit Factor: {metrics_dict['profit_factor']:.2f}")
    
    if 'avg_win_pct' in metrics_dict:
        print(f"Average Win: {metrics_dict['avg_win_pct']:.2f}%")
    
    if 'avg_loss_pct' in metrics_dict:
        print(f"Average Loss: {metrics_dict['avg_loss_pct']:.2f}%")
