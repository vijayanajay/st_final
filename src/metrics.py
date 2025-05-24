"""
metrics.py

Calculate performance metrics based on trade log and portfolio value series.
Task 23 focus: Basic return calculations (Total Return % and Annualized Return %)
"""
import pandas as pd
from typing import List, Dict


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
        Dictionary containing calculated metrics
        
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
    
    return {
        'total_return_pct': total_return_pct,
        'annualized_return_pct': annualized_return_pct
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
