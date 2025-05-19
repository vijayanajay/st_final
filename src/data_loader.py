"""
data_loader.py
Fetches historical stock data using yfinance.
"""
import logging
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    raise ImportError("yfinance is required. Please install it via requirements.txt.")

def fetch(ticker: str, period: str = "max") -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker and period using yfinance.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str, optional): Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.

    Returns:
        pd.DataFrame: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume']

    Raises:
        ValueError: If input parameters are invalid or data is empty.
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string.")
    if not period or not isinstance(period, str):
        raise ValueError("Period must be a non-empty string.")
    logging.info(f"Fetching data for {ticker} with period '{period}'")
    try:
        data = yf.Ticker(ticker).history(period=period)
    except Exception as e:
        logging.error(f"yfinance error: {e}")
        raise
    if data.empty:
        logging.warning(f"No data returned for {ticker} with period '{period}'")
        raise ValueError(f"No data found for {ticker} in given period.")
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in data.columns for col in required_cols):
        logging.error(f"Missing columns in data: {data.columns}")
        raise ValueError("Returned data missing required columns.")
    return data[required_cols]
