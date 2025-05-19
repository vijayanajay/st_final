import pandas as pd

def calculate_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
    """
    Calculate the Simple Moving Average (SMA) for a given column in a DataFrame.

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
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if not isinstance(window, int) or window <= 0:
        raise ValueError("Window size must be a positive integer.")

    sma = df[column].rolling(window=window, min_periods=window).mean()
    sma.name = f'sma_{window}'
    return sma
