# src/strategies.py
"""
This module will contain the logic for different trading strategies.
"""

import pandas as pd
import numpy as np
import logging

class BaseStrategy:
    """
    A base class for all trading strategies.
    """
    pass

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

def apply_strategy(df, strategy_params):
    """
    Apply a trading strategy to a DataFrame and generate buy/sell signals.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing price data and any required technical indicators.
    strategy_params : dict
        Dictionary containing strategy type and parameters.
        Must include 'strategy_type' key and 'parameters' dict.
    
    Returns:
    --------
    pandas.DataFrame
        Original DataFrame with added 'signal' column where:
        1 = buy signal
        -1 = sell signal
        0 = no signal/hold
    
    Raises:
    -------
    ValueError
        If strategy type is not supported or required parameters are missing.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Applying {strategy_params['strategy_type']} strategy")
    
    # Create a copy of the DataFrame to avoid modifying the original
    result_df = df.copy()
    
    # Initialize signal column with zeros (no signal)
    result_df['signal'] = 0
    
    strategy_type = strategy_params.get('strategy_type')
    params = strategy_params.get('parameters', {})
    
    if strategy_type == 'sma_crossover':
        # Check for required parameters
        required_params = ['fast_sma', 'slow_sma']
        for param in required_params:
            if param not in params:
                error_msg = f"Missing required parameter '{param}' for SMA crossover strategy"
                logger.error(error_msg)
                raise ValueError(error_msg)
          # Apply SMA crossover strategy
        signals = generate_sma_crossover_signals(
            result_df, 
            short_window_col=params['fast_sma'],
            long_window_col=params['slow_sma']
        )
        result_df['signal'] = signals
    else:
        error_msg = f"Unsupported strategy type: {strategy_type}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"Strategy applied, generated {(result_df['signal'] != 0).sum()} signals")
    return result_df
