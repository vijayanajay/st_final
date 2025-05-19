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

def _fetch_data(ticker: str, period: str) -> pd.DataFrame:
    try:
        data = yf.Ticker(ticker).history(period=period)
    except Exception as e:
        logging.error(f"yfinance error: {e}")
        raise
    if data.empty:
        logging.warning(f"No data returned for {ticker} with period '{period}'")
        raise ValueError(f"No data found for {ticker} in given period.")
    return data

@functools.lru_cache(maxsize=32)
def _cached_fetch_data(ticker: str, period: str) -> pd.DataFrame:
    return _fetch_data(ticker, period)

def fetch(
    ticker: str,
    period: str = "max",
    columns: Optional[List[str]] = None,
    use_cache: bool = True
) -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker and period using yfinance.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str, optional): Data period (e.g., '1y', '6mo', 'max'). Defaults to 'max'.
        columns (List[str], optional): Columns to return. Defaults to ['Open', 'High', 'Low', 'Close', 'Volume'].
        use_cache (bool, optional): Use in-memory cache for repeated queries. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with requested columns.

    Raises:
        ValueError: If input parameters are invalid or data is empty.
    """
    validate_ticker(ticker)
    validate_period(period)
    if columns is None:
        columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    logging.info(f"Fetching data for {ticker} with period '{period}' and columns {columns}")
    data = _cached_fetch_data(ticker, period) if use_cache else _fetch_data(ticker, period)
    validate_columns(data, columns)
    return data[columns]
