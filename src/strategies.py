# src/strategies.py
"""
This module will contain the logic for different trading strategies.
"""

import pandas as pd
import numpy as np
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Type

class BaseStrategy(ABC):
    """
    A base class for all trading strategies.
    
    This class serves as the foundation for implementing the Strategy Pattern,
    where different trading strategies will inherit from this base class and
    implement common interface methods for generating signals and evaluating performance.
    """
    
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        """
        Generate trading signals based on the strategy's logic.
        
        Args:
            df (pd.DataFrame): DataFrame containing price data and any required technical indicators.
            params (Dict[str, Any]): Dictionary containing strategy-specific parameters.
            
        Returns:
            pd.Series: Series with trading signals (1 for buy, -1 for sell, 0 for hold).
            
        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        pass
    
    @abstractmethod
    def get_required_parameters(self) -> List[str]:
        """
        Get the list of required parameters for this strategy.
        
        Returns:
            List[str]: List of required parameter names.
        """
        pass
    
    def validate_parameters(self, params: Dict[str, Any]) -> None:
        """
        Validate that all required parameters are present.
        
        Args:
            params (Dict[str, Any]): Dictionary containing strategy parameters.
            
        Raises:
            ValueError: If any required parameter is missing.
        """
        required_params = self.get_required_parameters()
        for param in required_params:
            if param not in params:
                error_msg = f"Missing required parameter '{param}' for {self.__class__.__name__}"
                logging.error(error_msg)
                raise ValueError(error_msg)


class SMACrossoverStrategy(BaseStrategy):
    """
    Strategy that generates signals based on SMA crossovers.
    
    Generates buy signals when the short-term SMA crosses above the long-term SMA,
    and sell signals when the short-term SMA crosses below the long-term SMA.
    """
    
    def get_required_parameters(self) -> List[str]:
        """
        Get the list of required parameters for the SMA crossover strategy.
        
        Returns:
            List[str]: List of required parameter names.
        """
        return ['fast_sma', 'slow_sma']
    
    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.Series:
        """
        Generate SMA crossover trading signals.
        
        Args:
            df (pd.DataFrame): DataFrame containing SMA feature columns.
            params (Dict[str, Any]): Dictionary containing parameters:
                - fast_sma (str): Name of the short window SMA column.
                - slow_sma (str): Name of the long window SMA column.
                
        Returns:
            pd.Series: Series with trading signals (1 for buy, -1 for sell, 0 for hold).
            
        Raises:
            ValueError: If required columns are missing from the input DataFrame.
        """
        # Validate parameters
        self.validate_parameters(params)
        
        short_window_col = params['fast_sma']
        long_window_col = params['slow_sma']
        
        # Validate required columns
        if not {short_window_col, long_window_col}.issubset(df.columns):
            raise ValueError(f"Input DataFrame must contain '{short_window_col}' and '{long_window_col}' columns.")
        
        # Initialize signals with 0 (HOLD)
        signals = pd.Series(0, index=df.index, name="signal")
        
        # Generate buy signals (short crosses above long)
        signals.loc[
            (df[short_window_col].shift(1) <= df[long_window_col].shift(1)) &
            (df[short_window_col] > df[long_window_col])
        ] = 1  # Buy signal
        
        # Generate sell signals (short crosses below long)
        signals.loc[
            (df[short_window_col].shift(1) >= df[long_window_col].shift(1)) &
            (df[short_window_col] < df[long_window_col])
        ] = -1  # Sell signal
        
        return signals


# Registry of available strategies
STRATEGY_REGISTRY: Dict[str, Type[BaseStrategy]] = {
    'sma_crossover': SMACrossoverStrategy,
}


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
        
    Note:
        This function is kept for backward compatibility.
        It is recommended to use the Strategy pattern with SMACrossoverStrategy instead.
    """
    strategy = SMACrossoverStrategy()
    params = {
        'fast_sma': short_window_col,
        'slow_sma': long_window_col
    }
    return strategy.generate_signals(df_with_features, params)


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
    
    # Check if strategy type is supported in the registry
    if strategy_type not in STRATEGY_REGISTRY:
        error_msg = f"Unsupported strategy type: {strategy_type}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Create an instance of the appropriate strategy class
    strategy_class = STRATEGY_REGISTRY[strategy_type]
    strategy = strategy_class()
    
    # Generate signals using the strategy
    signals = strategy.generate_signals(result_df, params)
    result_df['signal'] = signals
    
    logger.info(f"Strategy applied, generated {(result_df['signal'] != 0).sum()} signals")
    return result_df
