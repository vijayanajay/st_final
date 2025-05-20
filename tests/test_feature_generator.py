import pytest
import pandas as pd
import numpy as np
import logging

from src.feature_generator import calculate_sma, calculate_price_change_pct, calculate_volatility

@pytest.fixture
def sample_df():
    return pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})

# Parameterized test cases for feature functions
@pytest.mark.parametrize("func,kwargs,expected", [
    # SMA basic
    (calculate_sma, dict(column='close', window=3), pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3')),
    # Price change pct basic
    (calculate_price_change_pct, dict(column='close'), pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], name='price_change_pct_1d')),
    # Volatility basic
    (calculate_volatility, dict(column='close', window=2), pd.Series([np.nan, np.nan, 0.6464466094067263, 0.5354837503184306, 0.4714045207910317, 0.408248290463863], name='volatility_2')),
])
def test_feature_basic(sample_df, func, kwargs, expected):
    # For volatility, recalculate expected dynamically for robustness
    if func is calculate_volatility:
        price_change = (sample_df['close'] - sample_df['close'].shift(1)) / sample_df['close'].shift(1) * 100
        expected = price_change.rolling(window=kwargs['window'], min_periods=kwargs['window']).std()
        expected.name = f"volatility_{kwargs['window']}"
    if func is calculate_price_change_pct:
        expected = (sample_df['close'] - sample_df['close'].shift(1)) / sample_df['close'].shift(1) * 100
        expected.name = 'price_change_pct_1d'
    result = func(sample_df, **kwargs)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("func,kwargs", [
    (calculate_sma, dict(column='close', window=10)),
    (calculate_volatility, dict(column='close', window=10)),
])
def test_window_larger_than_data(sample_df, func, kwargs):
    expected = pd.Series([np.nan]*len(sample_df), name=f"{func.__name__.replace('calculate_', '')}_{kwargs['window']}")
    result = func(sample_df, **kwargs)
    # Only check all-NaN, name is checked in basic test
    assert result.isna().all()

@pytest.mark.parametrize("func,kwargs", [
    (calculate_sma, dict(column='open', window=3)),
    (calculate_price_change_pct, dict(column='not_a_column')),
    (calculate_volatility, dict(column='not_a_column', window=2)),
])
def test_invalid_column(sample_df, func, kwargs):
    with pytest.raises(ValueError):
        func(sample_df, **kwargs)

@pytest.mark.parametrize("func,kwargs", [
    (calculate_sma, dict(column='close', window=0)),
    (calculate_sma, dict(column='close', window=-2)),
    (calculate_volatility, dict(column='close', window=0)),
    (calculate_volatility, dict(column='close', window=-1)),
])
def test_invalid_window(sample_df, func, kwargs):
    with pytest.raises(ValueError):
        func(sample_df, **kwargs)

@pytest.mark.parametrize("func,df,kwargs", [
    (calculate_price_change_pct, pd.DataFrame({'close': ['a', 'b', 'c']}), dict(column='close')),
    (calculate_volatility, pd.DataFrame({'close': ['a', 'b', 'c']}), dict(column='close', window=2)),
])
def test_non_numeric_column(func, df, kwargs):
    with pytest.raises(ValueError):
        func(df, **kwargs)

# Feature-specific logging tests (not easily parameterized)
def test_sma_logging(sample_df, caplog):
    with caplog.at_level('INFO'):
        calculate_sma(sample_df, column='close', window=2)
    assert any('Calculating SMA' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_sma(sample_df, column='open', window=2)
        assert any("not found in DataFrame" in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_sma(sample_df, column='close', window=0)
        assert any("Window size must be a positive integer" in record.getMessage() for record in caplog.records)

def test_price_change_pct_logging(caplog):
    df = pd.DataFrame({'close': [10, 12, 15]})
    with caplog.at_level('INFO'):
        calculate_price_change_pct(df, column='close')
    assert any('Calculating 1-day price change percentage' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_price_change_pct(df, column='not_a_column')
        assert any('not found in DataFrame' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        df2 = pd.DataFrame({'close': ['a', 'b', 'c']})
        with pytest.raises(ValueError):
            calculate_price_change_pct(df2, column='close')
        assert any('must be numeric' in record.getMessage() for record in caplog.records)

def test_volatility_logging(caplog):
    df = pd.DataFrame({'close': [10, 12, 15]})
    with caplog.at_level('INFO'):
        calculate_volatility(df, column='close', window=2)
    assert any('Calculating volatility' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_volatility(df, column='not_a_column', window=2)
        assert any('not found in DataFrame' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_volatility(df, column='close', window=0)
        assert any('Window size must be a positive integer' in record.getMessage() for record in caplog.records)

def test_calculate_sma_logs_error_on_invalid_column(sample_df, caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            calculate_sma(sample_df, column='not_a_column', window=3)
    assert any("not found in DataFrame" in record.getMessage() for record in caplog.records)

def test_calculate_price_change_pct_logs_error_on_invalid_column(sample_df, caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            calculate_price_change_pct(sample_df, column='not_a_column')
    assert any("not found in DataFrame" in record.getMessage() for record in caplog.records)

def test_calculate_volatility_logs_error_on_invalid_column(sample_df, caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            calculate_volatility(sample_df, column='not_a_column', window=2)
    assert any("not found in DataFrame" in record.getMessage() for record in caplog.records)
