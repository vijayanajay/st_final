import pytest
import pandas as pd
from src import data_loader
import yfinance

class DummyTicker:
    def __init__(self, ticker):
        self.ticker = ticker
        self.called_with = None
    def history(self, period=None):
        self.called_with = period
        return pd.DataFrame({
            'Open': [1.0], 'High': [1.1], 'Low': [0.9], 'Close': [1.05], 'Volume': [1000]
        })

def test_fetch_calls_yfinance_and_returns_dataframe(monkeypatch):
    calls = {}
    def dummy_ticker_factory(ticker):
        calls['ticker'] = ticker
        return DummyTicker(ticker)
    monkeypatch.setattr(yfinance, 'Ticker', dummy_ticker_factory)

    df = data_loader.fetch('AAPL', period='1y')

    # Verify yfinance.Ticker was called with correct ticker
    assert calls['ticker'] == 'AAPL'
    # Verify DataFrame structure
    assert isinstance(df, pd.DataFrame)
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        assert col in df.columns
    assert not df.empty
