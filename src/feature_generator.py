import pandas as pd
import logging

def add_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
    """
    Add Simple Moving Average (SMA) to the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing price data.
        column (str): Name of the column to calculate SMA on.
        window (int): Window size for the moving average. Must be > 0.

    Returns:
        pd.Series: Series containing the SMA values, named as 'sma_{window}'.

    Raises:
        ValueError: If the column does not exist or window is invalid.
    """
    if not isinstance(df, pd.DataFrame):
        logging.error("Input must be a pandas DataFrame.")
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        logging.error(f"Column '{column}' not found in DataFrame.")
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if not isinstance(window, int) or window <= 0:
        logging.error("Window size must be a positive integer.")
        raise ValueError("Window size must be a positive integer.")

    logging.info(f"Calculating SMA: column={column}, window={window}")
    sma = df[column].rolling(window=window, min_periods=window).mean()
    sma.name = f'sma_{window}'
    return sma

def add_price_change_pct_1d(df: pd.DataFrame, column: str = "close") -> pd.Series:
    """
    Add 1-day price change percentage to the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing price data.
        column (str): Name of the column to calculate price change percentage on. Defaults to 'close'.

    Returns:
        pd.Series: Series containing the 1-day price change percentage, named as 'price_change_pct_1d'.

    Raises:
        ValueError: If the column does not exist or is not numeric.
    """
    if not isinstance(df, pd.DataFrame):
        logging.error("Input must be a pandas DataFrame.")
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        logging.error(f"Column '{column}' not found in DataFrame.")
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        logging.error(f"Column '{column}' must be numeric.")
        raise ValueError(f"Column '{column}' must be numeric.")
    logging.info(f"Calculating 1-day price change percentage: column={column}")
    pct = (df[column] - df[column].shift(1)) / df[column].shift(1) * 100
    pct.name = 'price_change_pct_1d'
    return pct

def add_volatility_nday(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series:
    """
    Add n-day rolling volatility to the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing price data.
        column (str): Name of the column to calculate volatility on. Defaults to 'close'.
        window (int): Window size for the rolling standard deviation. Must be > 0.

    Returns:
        pd.Series: Series containing the rolling volatility, named as 'volatility_{window}'.

    Raises:
        ValueError: If the column does not exist, is not numeric, or window is invalid.
    """
    if not isinstance(df, pd.DataFrame):
        logging.error("Input must be a pandas DataFrame.")
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        logging.error(f"Column '{column}' not found in DataFrame.")
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        logging.error(f"Column '{column}' must be numeric.")
        raise ValueError(f"Column '{column}' must be numeric.")
    if not isinstance(window, int) or window <= 0:
        logging.error("Window size must be a positive integer.")
        raise ValueError("Window size must be a positive integer.")
    logging.info(f"Calculating volatility: column={column}, window={window}")
    price_change = (df[column] - df[column].shift(1)) / df[column].shift(1) * 100
    volatility = price_change.rolling(window=window, min_periods=window).std()
    volatility.name = f'volatility_{window}'
    return volatility

# Backward compatibility aliases for tests
def calculate_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
    """
    This is an alias for add_sma provided for backward compatibility with tests.
    
    See add_sma for full documentation.
    """
    return add_sma(df, column, window)

def calculate_price_change_pct(df: pd.DataFrame, column: str = "close") -> pd.Series:
    """
    This is an alias for add_price_change_pct_1d provided for backward compatibility with tests.
    
    See add_price_change_pct_1d for full documentation.
    """
    return add_price_change_pct_1d(df, column)

def calculate_volatility(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series:
    """
    This is an alias for add_volatility_nday provided for backward compatibility with tests.
    
    See add_volatility_nday for full documentation.
    """
    return add_volatility_nday(df, column, window)

def generate_features(df: pd.DataFrame, feature_config: dict) -> pd.DataFrame:
    """
    Orchestrator to generate all features as specified in feature_config.

    Args:
        df (pd.DataFrame): Input DataFrame.
        feature_config (dict): Dict specifying which features to add and their parameters.

    Returns:
        pd.DataFrame: DataFrame with new feature columns added.
    """
    for feature, params in feature_config.items():
        if feature == "sma":
            df = df.join(add_sma(df, **params))
        elif feature == "price_change_pct_1d":
            df = df.join(add_price_change_pct_1d(df, **params))
        elif feature == "volatility_nday":
            df = df.join(add_volatility_nday(df, **params))
        else:
            logging.warning(f"Feature '{feature}' is not recognized and will be ignored.")
    return df
