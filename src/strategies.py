# src/strategies.py
"""
This module will contain the logic for different trading strategies.
"""

class BaseStrategy:
    """
    A base class for all trading strategies.
    """
    pass

import pandas as pd
import numpy as np

def generate_sma_crossover_signals(data: pd.DataFrame, short_window: int, long_window: int) -> pd.Series:
    """
    Generates trading signals based on SMA crossover.

    Args:
        data (pd.DataFrame): DataFrame with 'close', 'SMA_short', and 'SMA_long' columns.
        short_window (int): The short moving average window (for context, not direct use in this version).
        long_window (int): The long moving average window (for context, not direct use in this version).

    Returns:
        pd.Series: A series of trading signals (1 for BUY, -1 for SELL, 0 for HOLD).
    """
    # Validate required columns
    if not {'SMA_short', 'SMA_long'}.issubset(data.columns):
        raise ValueError("Input DataFrame must contain 'SMA_short' and 'SMA_long' columns.")

    signal = pd.Series(0, index=data.index, name="signal")
    prev_short = data['SMA_short'].shift(1)
    prev_long = data['SMA_long'].shift(1)

    # Buy: short crosses above long
    buy = (prev_short <= prev_long) & (data['SMA_short'] > data['SMA_long'])
    # Sell: short crosses below long
    sell = (prev_short >= prev_long) & (data['SMA_short'] < data['SMA_long'])

    signal[buy] = 1
    signal[sell] = -1
    return signal
