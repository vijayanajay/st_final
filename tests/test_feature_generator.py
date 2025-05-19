import pytest
import pandas as pd
import numpy as np
import logging

from src.feature_generator import calculate_sma, calculate_price_change_pct

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15]
    })

def test_sma_basic(sample_df):
    result = calculate_sma(sample_df, column='close', window=3)
    expected = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3')
    pd.testing.assert_series_equal(result, expected)

def test_sma_window_larger_than_data(sample_df):
    result = calculate_sma(sample_df, column='close', window=10)
    expected = pd.Series([np.nan]*6, name='sma_10')
    pd.testing.assert_series_equal(result, expected)

def test_sma_missing_column(sample_df):
    with pytest.raises(ValueError):
        calculate_sma(sample_df, column='open', window=3)

def test_sma_invalid_window(sample_df):
    with pytest.raises(ValueError):
        calculate_sma(sample_df, column='close', window=0)
    with pytest.raises(ValueError):
        calculate_sma(sample_df, column='close', window=-2)

def test_sma_nan_handling():
    df = pd.DataFrame({'close': [np.nan, 2, 3, 4, 5]})
    result = calculate_sma(df, column='close', window=2)
    expected = pd.Series([np.nan, np.nan, 2.5, 3.5, 4.5], name='sma_2')
    pd.testing.assert_series_equal(result, expected)

def test_sma_logging(sample_df, caplog):
    # calculate_sma should emit log messages for info and errors
    with caplog.at_level('INFO'):
        calculate_sma(sample_df, column='close', window=2)
    assert any('Calculating SMA' in msg for msg in caplog.messages)

    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_sma(sample_df, column='open', window=2)
        assert any("not found in DataFrame" in msg for msg in caplog.messages)

    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_sma(sample_df, column='close', window=0)
        assert any("Window size must be a positive integer" in msg for msg in caplog.messages)

def test_price_change_pct_basic():
    df = pd.DataFrame({'close': [10, 12, 15, 15, 10]})
    result = calculate_price_change_pct(df, column='close')
    expected = pd.Series([np.nan, 20.0, 25.0, 0.0, -33.33333333333333], name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)

def test_price_change_pct_nan_handling():
    df = pd.DataFrame({'close': [np.nan, 10, 12, np.nan, 15]})
    result = calculate_price_change_pct(df, column='close')
    expected = pd.Series([np.nan, np.nan, 20.0, np.nan, np.nan], name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)

def test_price_change_pct_invalid_column():
    df = pd.DataFrame({'close': [10, 12, 15]})
    with pytest.raises(ValueError):
        calculate_price_change_pct(df, column='not_a_column')

def test_price_change_pct_non_numeric():
    df = pd.DataFrame({'close': ['a', 'b', 'c']})
    with pytest.raises(ValueError):
        calculate_price_change_pct(df, column='close')

def test_price_change_pct_single_row():
    df = pd.DataFrame({'close': [10]})
    result = calculate_price_change_pct(df, column='close')
    expected = pd.Series([np.nan], name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)

def test_price_change_pct_logging(caplog):
    df = pd.DataFrame({'close': [10, 12, 15]})
    with caplog.at_level('INFO'):
        calculate_price_change_pct(df, column='close')
    assert any('Calculating 1-day price change percentage' in msg for msg in caplog.messages)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            calculate_price_change_pct(df, column='not_a_column')
        assert any('not found in DataFrame' in msg for msg in caplog.messages)
    with caplog.at_level('ERROR'):
        df2 = pd.DataFrame({'close': ['a', 'b', 'c']})
        with pytest.raises(ValueError):
            calculate_price_change_pct(df2, column='close')
        assert any('must be numeric' in msg for msg in caplog.messages)
