import pytest
import pandas as pd
from src import data_loader
import yfinance

class DummyTicker:
    def __init__(self, ticker):
        self.ticker = ticker
        self.called_with = None
        self.history_call_count = 0
    def history(self, period=None, interval=None):
        self.called_with = period
        self.history_call_count += 1
        return pd.DataFrame({
            'Open': [1.0], 'High': [1.1], 'Low': [0.9], 'Close': [1.05], 'Volume': [1000], 'Adj Close': [1.04]
        })

def test_fetch_calls_yfinance_and_returns_dataframe(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    calls = {}
    def dummy_ticker_factory(ticker):
        calls['ticker'] = ticker
        return DummyTicker(ticker)
    monkeypatch.setattr(yfinance, 'Ticker', dummy_ticker_factory)

    df = data_loader.fetch('RELIANCE.NS', period='1y')

    # Verify yfinance.Ticker was called with correct ticker
    assert calls['ticker'] == 'RELIANCE.NS'
    # Verify DataFrame structure
    assert isinstance(df, pd.DataFrame)
    for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
        assert col in df.columns
    assert not df.empty

def test_fetch_validates_ticker(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    monkeypatch.setattr(yfinance, 'Ticker', DummyTicker)
    with pytest.raises(ValueError):
        data_loader.fetch('', period='1y')
    with pytest.raises(ValueError):
        data_loader.fetch(None, period='1y')

def test_fetch_validates_period(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    monkeypatch.setattr(yfinance, 'Ticker', DummyTicker)
    with pytest.raises(ValueError):
        data_loader.fetch('RELIANCE.NS', period='')
    with pytest.raises(ValueError):
        data_loader.fetch('RELIANCE.NS', period=None)

def test_fetch_validates_columns(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    class DummyTickerMissingCol:
        def __init__(self, ticker): pass
        def history(self, period=None, interval=None):
            return pd.DataFrame({'Open': [1.0]})
    monkeypatch.setattr(yfinance, 'Ticker', DummyTickerMissingCol)
    with pytest.raises(ValueError):
        data_loader.fetch('RELIANCE.NS', period='1y', columns=['Open', 'Close'])

def test_fetch_parameterized_columns(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    monkeypatch.setattr(yfinance, 'Ticker', DummyTicker)
    df = data_loader.fetch('RELIANCE.NS', period='1y', columns=['Open', 'Close'])
    assert list(df.columns) == ['Open', 'Close']

def test_fetch_caching(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    call_counter = {'count': 0}
    class DummyTickerCount:
        def __init__(self, ticker): pass
        def history(self, period=None, interval=None):
            call_counter['count'] += 1
            return pd.DataFrame({'Open': [1.0], 'High': [1.1], 'Low': [0.9], 'Close': [1.05], 'Volume': [1000], 'Adj Close': [1.04]})
    monkeypatch.setattr(yfinance, 'Ticker', DummyTickerCount)
    data_loader.fetch('RELIANCE.NS', period='1y')
    data_loader.fetch('RELIANCE.NS', period='1y')  # Should use cache
    assert call_counter['count'] == 1
    data_loader.fetch('RELIANCE.NS', period='1y', use_cache=False)  # Should not use cache
    assert call_counter['count'] == 2

def test_fetch_handles_yfinance_error(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    class DummyTickerError:
        def __init__(self, ticker): pass
        def history(self, period=None, interval=None):
            raise Exception('yfinance error')
    monkeypatch.setattr(yfinance, 'Ticker', DummyTickerError)
    with pytest.raises(Exception):
        data_loader.fetch('RELIANCE.NS', period='1y', use_cache=False)

def test_fetch_handles_empty_data(monkeypatch):
    data_loader._cached_fetch_data.cache_clear()
    class DummyTickerEmpty:
        def __init__(self, ticker): pass
        def history(self, period=None, interval=None):
            return pd.DataFrame()
    monkeypatch.setattr(yfinance, 'Ticker', DummyTickerEmpty)
    with pytest.raises(ValueError):
        data_loader.fetch('RELIANCE.NS', period='1y', use_cache=False)

def test_fetch_all_nan_column(monkeypatch, caplog):
    data_loader._cached_fetch_data.cache_clear()
    class DummyTickerAllNaN:
        def __init__(self, ticker): pass
        def history(self, period=None, interval=None):
            return pd.DataFrame({
                'Open': [float('nan')],
                'High': [1.1],
                'Low': [0.9],
                'Close': [1.05],
                'Volume': [1000]
            })
    monkeypatch.setattr(yfinance, 'Ticker', DummyTickerAllNaN)
    with caplog.at_level('WARNING'):
        with pytest.raises(ValueError):
            data_loader.fetch('RELIANCE.NS', period='1y', columns=['Open', 'High', 'Low', 'Close', 'Volume'], use_cache=False)
        assert any('all-NaN' in record.getMessage() for record in caplog.records)

def test_fetch_logs_error_on_invalid_input(monkeypatch, caplog):
    data_loader._cached_fetch_data.cache_clear()
    monkeypatch.setattr(yfinance, 'Ticker', DummyTicker)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            data_loader.fetch('', period='1y')
        assert any('Ticker' in record.getMessage() for record in caplog.records)

@pytest.mark.skip(reason="Integration test: requires network and real API")
def test_fetch_integration_real_api():
    data_loader._cached_fetch_data.cache_clear()
    df = data_loader.fetch('RELIANCE.NS', period='1d', columns=['Open', 'Close'], use_cache=False)
    assert isinstance(df, pd.DataFrame)
    assert 'Open' in df.columns and 'Close' in df.columns
    assert not df.empty

def test_fetch_data_signature_and_behavior():
    import inspect
    from src import data_loader
    sig = inspect.signature(data_loader.fetch_data)
    assert list(sig.parameters.keys()) == ["ticker", "period", "interval"]
    # ...additional tests for correct behavior, error handling, and logging...
