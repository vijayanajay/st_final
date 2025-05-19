import pytest
import pandas as pd
import numpy as np
import logging

from src.feature_generator import calculate_sma

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
