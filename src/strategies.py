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

def generate_sma_crossover_signals(df_with_features: pd.DataFrame, 
                              short_window_col: str = "SMA_short", 
                              long_window_col: str = "SMA_long") -> pd.Series:
    """
    Generate SMA crossover trading signals.

    Args:
        df_with_features (pd.DataFrame): DataFrame containing SMA feature columns.
        short_window_col (str, optional): Name of the short window SMA column. Defaults to "SMA_short".
        long_window_col (str, optional): Name of the long window SMA column. Defaults to "SMA_long".

    Returns:
        pd.Series: Series with trading signals (1 for buy, -1 for sell, 0 for hold).
    
    Raises:
        ValueError: If required columns are missing from the input DataFrame.
    """
    # Validate required columns
    if not {short_window_col, long_window_col}.issubset(df_with_features.columns):
        raise ValueError(f"Input DataFrame must contain '{short_window_col}' and '{long_window_col}' columns.")

    # Initialize signals with 0 (HOLD)
    signals = pd.Series(0, index=df_with_features.index, name="signal")

    # Generate buy signals (short crosses above long)
    signals.loc[
        (df_with_features[short_window_col].shift(1) <= df_with_features[long_window_col].shift(1)) &
        (df_with_features[short_window_col] > df_with_features[long_window_col])
    ] = 1  # Buy signal

    # Generate sell signals (short crosses below long)
    signals.loc[
        (df_with_features[short_window_col].shift(1) >= df_with_features[long_window_col].shift(1)) &
        (df_with_features[short_window_col] < df_with_features[long_window_col])
    ] = -1  # Sell signal

    return signals
