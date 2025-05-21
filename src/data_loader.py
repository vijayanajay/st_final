"""
data_loader.py
Fetches historical stock data using yfinance.
"""
import logging
import pandas as pd
import functools
from typing import List, Optional

try:
    import yfinance as yf
except ImportError:
    raise ImportError("yfinance is required. Please install it via requirements.txt.")

def validate_ticker(ticker: str) -> None:
    if not ticker or not isinstance(ticker, str):
        logging.error("Ticker must be a non-empty string.")
        raise ValueError("Ticker must be a non-empty string.")

def validate_period(period: str) -> None:
    if not period or not isinstance(period, str):
        logging.error("Period must be a non-empty string.")
        raise ValueError("Period must be a non-empty string.")

def validate_columns(data: pd.DataFrame, required_cols: List[str]) -> None:
    missing = [col for col in required_cols if col not in data.columns]
    if missing:
        logging.error(f"Missing columns in data: {missing}")
        raise ValueError(f"Returned data missing required columns: {missing}")
    # Check for all-NaN columns
    for col in required_cols:
        if col in data.columns and data[col].isna().all():
            logging.warning(f"Column '{col}' contains all-NaN values.")
            raise ValueError(f"Column '{col}' contains all-NaN values.")

def _fetch_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    try:
        data = yf.Ticker(ticker).history(period=period, interval=interval)
    except Exception as e:
        logging.error(f"yfinance error: {e}")
        raise
    if data.empty:
        logging.warning(f"No data returned for {ticker} with period '{period}' and interval '{interval}'")
        raise ValueError(f"No data found for {ticker} in given period and interval.")
    return data

@functools.lru_cache(maxsize=32)
def _cached_fetch_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    return _fetch_data(ticker, period, interval)

def fetch_data(
    ticker: str,
    period: str = "max",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker, period, and interval using yfinance.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str, optional): Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.
        interval (str, optional): Data interval (e.g., '1d', '1wk'). Defaults to '1d'.

    Returns:
        pd.DataFrame: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].

    Raises:
        ValueError: If input parameters are invalid or data is empty.

    Logging:
        Logs key events, errors, and warnings for observability.
    """
    validate_ticker(ticker)
    validate_period(period)
    logging.info(f"Fetching data for {ticker} with period '{period}' and interval '{interval}'")
    data = _cached_fetch_data(ticker, period, interval)
    validate_columns(data, ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    return data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

def fetch(
    ticker: str,
    period: str = "1y",
    columns: List[str] = None,
    use_cache: bool = True
) -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker and period.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str, optional): Data period (e.g., '1y', '6mo', 'max'). Defaults to '1y'.
        columns (List[str], optional): List of columns to return. If None, returns all columns.
        use_cache (bool, optional): Whether to use cached data if available. Defaults to True.
        
    Returns:
        pd.DataFrame: DataFrame with requested columns.
        
    Raises:
        ValueError: If input parameters are invalid or data is empty.
    """
    validate_ticker(ticker)
    validate_period(period)
    
    logging.info(f"Fetching data for {ticker} with period '{period}'")
    
    if use_cache:
        data = _cached_fetch_data(ticker, period, "1d")
    else:
        data = _fetch_data(ticker, period, "1d")
    
    # If columns specified, validate they exist
    if columns:
        validate_columns(data, columns)
        return data[columns]
    else:
        validate_columns(data, ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        return data
