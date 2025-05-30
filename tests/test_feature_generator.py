import pytest
import pandas as pd
import numpy as np
import logging

# Import primary API functions
from src.feature_generator import add_sma, add_price_change_pct_1d, add_volatility_nday
# Import legacy aliases for delegation tests
from src.feature_generator import calculate_sma, calculate_price_change_pct, calculate_volatility

@pytest.fixture
def sample_df():
    return pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})

# Parameterized test cases for primary API feature functions
@pytest.mark.parametrize("func,kwargs,expected", [
    # SMA basic
    (add_sma, dict(column='close', window=3), pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3')),
    # Price change pct basic
    (add_price_change_pct_1d, dict(column='close'), pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], name='price_change_pct_1d')),
    # Volatility basic
    (add_volatility_nday, dict(column='close', window=2), pd.Series([np.nan, np.nan, 0.6428243465332251, 0.5356869554443592, 0.45327357768369, 0.3885202094431676], name='volatility_2')),
])
def test_feature_basic(sample_df, func, kwargs, expected):
    # Use static pre-calculated expected values for all functions
    # No dynamic recalculation to ensure independent verification
    result = func(sample_df, **kwargs)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("func,kwargs", [
    (add_sma, dict(column='close', window=10)),
    (add_volatility_nday, dict(column='close', window=10)),
])
def test_window_larger_than_data(sample_df, func, kwargs):
    expected_name = 'sma_10' if func == add_sma else 'volatility_10'
    expected = pd.Series([np.nan]*len(sample_df), name=expected_name)
    result = func(sample_df, **kwargs)
    # Only check all-NaN, name is checked in basic test
    assert result.isna().all()



@pytest.mark.parametrize("func,df,kwargs", [
    (add_sma, pd.DataFrame({'close': ['a', 'b', 'c']}), dict(column='close', window=2)),
    (add_price_change_pct_1d, pd.DataFrame({'close': ['a', 'b', 'c']}), dict(column='close')),
    (add_volatility_nday, pd.DataFrame({'close': ['a', 'b', 'c']}), dict(column='close', window=2)),
])
def test_non_numeric_column(func, df, kwargs):
    with pytest.raises(ValueError):
        func(df, **kwargs)

# Feature-specific logging tests (not easily parameterized)
def test_sma_logging(sample_df, caplog):
    with caplog.at_level('INFO'):
        add_sma(sample_df, column='close', window=2)
    assert any('Calculating SMA' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            add_sma(sample_df, column='open', window=2)
        assert any("not found in DataFrame" in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            add_sma(sample_df, column='close', window=0)
        assert any("Window size must be a positive integer" in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        df_non_numeric = pd.DataFrame({'close': ['a', 'b', 'c']})
        with pytest.raises(ValueError):
            add_sma(df_non_numeric, column='close', window=2)
        assert any("must be numeric for SMA calculation" in record.getMessage() for record in caplog.records)

def test_price_change_pct_logging(caplog):
    df = pd.DataFrame({'close': [10, 12, 15]})
    with caplog.at_level('INFO'):
        add_price_change_pct_1d(df, column='close')
    assert any('Calculating 1-day price change percentage' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            add_price_change_pct_1d(df, column='not_a_column')
        assert any('not found in DataFrame' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        df2 = pd.DataFrame({'close': ['a', 'b', 'c']})
        with pytest.raises(ValueError):
            add_price_change_pct_1d(df2, column='close')
        assert any('must be numeric' in record.getMessage() for record in caplog.records)

def test_volatility_logging(caplog):
    df = pd.DataFrame({'close': [10, 12, 15]})
    with caplog.at_level('INFO'):
        add_volatility_nday(df, column='close', window=2)
    assert any('Calculating volatility' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            add_volatility_nday(df, column='not_a_column', window=2)
        assert any('not found in DataFrame' in record.getMessage() for record in caplog.records)
    with caplog.at_level('ERROR'):
        with pytest.raises(ValueError):
            add_volatility_nday(df, column='close', window=0)
        assert any('Window size must be a positive integer' in record.getMessage() for record in caplog.records)

# Tests for legacy function delegation
@pytest.mark.parametrize("legacy_func, primary_func, kwargs", [
    (calculate_sma, add_sma, dict(column='close', window=3)),
    (calculate_price_change_pct, add_price_change_pct_1d, dict(column='close')),
    (calculate_volatility, add_volatility_nday, dict(column='close', window=4)),
])
def test_legacy_function_delegation(sample_df, legacy_func, primary_func, kwargs):
    """Test that legacy functions correctly delegate to their primary API counterparts."""
    # Call both functions and verify they produce identical results
    legacy_result = legacy_func(sample_df, **kwargs)
    primary_result = primary_func(sample_df, **kwargs)
    
    # Verify the results are identical
    pd.testing.assert_series_equal(legacy_result, primary_result)
    
    # Ensure the legacy functions are properly documented as aliases
    assert "alias" in legacy_func.__doc__.lower()
    assert primary_func.__name__ in legacy_func.__doc__

def test_add_sma_signature_and_behavior():
    import inspect
    from src import feature_generator
    sig = inspect.signature(feature_generator.add_sma)
    assert list(sig.parameters.keys()) == ["df", "column", "window"]
    # This test only checks the function signature. Behavior, error handling, and logging are covered in dedicated test functions like test_add_sma_with_valid_inputs, test_add_sma_raises_appropriate_errors, and test_sma_logging.

def test_add_sma_with_valid_inputs():
    """Test add_sma function with various valid inputs."""
    from src.feature_generator import add_sma
    # Basic test case
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    result = add_sma(df, 'close', 3)
    expected = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3')
    pd.testing.assert_series_equal(result, expected)
    
    # Different column name
    df = pd.DataFrame({'price': [10, 11, 12, 13, 14, 15]})
    result = add_sma(df, 'price', 2)
    expected = pd.Series([np.nan, 10.5, 11.5, 12.5, 13.5, 14.5], name='sma_2')
    pd.testing.assert_series_equal(result, expected)
    
    # Different window size
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    result = add_sma(df, 'close', 4)
    expected = pd.Series([np.nan, np.nan, np.nan, 11.5, 12.5, 13.5], name='sma_4')
    pd.testing.assert_series_equal(result, expected)

def test_add_sma_with_edge_cases():
    """Test add_sma function with edge cases like empty DataFrame and DataFrame with NaNs."""
    from src.feature_generator import add_sma
    # Empty DataFrame
    df = pd.DataFrame({'close': []})
    result = add_sma(df, 'close', 3)
    expected = pd.Series([], name='sma_3', dtype='float64')
    pd.testing.assert_series_equal(result, expected)
    
    # DataFrame with NaNs not at the start
    df = pd.DataFrame({'close': [10, np.nan, 12, 13, np.nan, 15]})
    result = add_sma(df, 'close', 2)
    expected = pd.Series([np.nan, np.nan, np.nan, 12.5, np.nan, np.nan], name='sma_2')
    pd.testing.assert_series_equal(result, expected)
    
    # DataFrame with different data types (should still work if numeric)
    df = pd.DataFrame({'close': [10, 11.5, 12, 13.7, 14, 15.2]})
    result = add_sma(df, 'close', 3)
    expected = pd.Series([np.nan, np.nan, 11.166666666666666, 12.4, 13.233333333333334, 14.3], name='sma_3')
    pd.testing.assert_series_equal(result, expected)

def test_add_sma_raises_appropriate_errors():
    """Test add_sma function raises appropriate errors for invalid inputs."""
    from src.feature_generator import add_sma
    
    # Invalid DataFrame type
    with pytest.raises(ValueError, match="Input must be a pandas DataFrame"):
        add_sma("not_a_dataframe", 'close', 3)
    
    # Non-existent column
    df = pd.DataFrame({'close': [10, 11, 12]})
    with pytest.raises(ValueError, match="Column 'not_a_column' not found"):
        add_sma(df, 'not_a_column', 3)
    
    # Invalid window values
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        add_sma(df, 'close', 0)
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        add_sma(df, 'close', -1)
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        add_sma(df, 'close', "3")

def test_add_price_change_pct_1d_signature_and_behavior():
    import inspect
    from src import feature_generator
    sig = inspect.signature(feature_generator.add_price_change_pct_1d)
    assert list(sig.parameters.keys()) == ["df", "column"]
    # This test only checks the function signature. Behavior, error handling, and logging are covered in dedicated test functions like test_add_price_change_pct_1d_with_valid_inputs, test_add_price_change_pct_1d_raises_appropriate_errors, and test_price_change_pct_1d_logging.

def test_add_price_change_pct_1d_with_valid_inputs():
    """Test add_price_change_pct_1d function with various valid inputs."""
    from src.feature_generator import add_price_change_pct_1d
    
    # Basic test case
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    result = add_price_change_pct_1d(df, 'close')
    expected = pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], 
                         name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)
    
    # Different column name
    df = pd.DataFrame({'price': [10, 11, 12, 13, 14, 15]})
    result = add_price_change_pct_1d(df, 'price')
    expected = pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], 
                         name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)
    
    # Default column parameter
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    result = add_price_change_pct_1d(df)  # Should use 'close' as default
    expected = pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], 
                         name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)

def test_add_price_change_pct_1d_with_edge_cases():
    """Test add_price_change_pct_1d function with edge cases."""
    from src.feature_generator import add_price_change_pct_1d
    
    # Empty DataFrame
    df = pd.DataFrame({'close': []})
    result = add_price_change_pct_1d(df)
    expected = pd.Series([], name='price_change_pct_1d', dtype='float64')
    pd.testing.assert_series_equal(result, expected)
    
    # DataFrame with NaNs not at the start
    df = pd.DataFrame({'close': [10, np.nan, 12, 13, np.nan, 15]})
    result = add_price_change_pct_1d(df)
    # First value is NaN (no previous value), second result is NaN (previous is NaN),
    # third result is based on 12/NaN, etc.
    expected = pd.Series([np.nan, np.nan, np.nan, 8.333333333333332, np.nan, np.nan], 
                        name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)
    
    # DataFrame with zero values (test division by zero handling)
    df = pd.DataFrame({'close': [0, 10, 0, 15]})
    result = add_price_change_pct_1d(df)
    # Expected: [NaN, infinity, -100, infinity]
    expected = pd.Series([np.nan, float('inf'), -100.0, float('inf')], name='price_change_pct_1d')
    pd.testing.assert_series_equal(result, expected)

def test_add_price_change_pct_1d_raises_appropriate_errors():
    """Test add_price_change_pct_1d function raises appropriate errors for invalid inputs."""
    from src.feature_generator import add_price_change_pct_1d
    
    # Invalid DataFrame type
    with pytest.raises(ValueError, match="Input must be a pandas DataFrame"):
        add_price_change_pct_1d("not_a_dataframe")
    
    # Non-existent column
    df = pd.DataFrame({'close': [10, 11, 12]})
    with pytest.raises(ValueError, match="Column 'not_a_column' not found"):
        add_price_change_pct_1d(df, 'not_a_column')
    
    # Non-numeric column
    df = pd.DataFrame({'close': ['a', 'b', 'c']})
    with pytest.raises(ValueError, match="Column 'close' must be numeric"):
        add_price_change_pct_1d(df)

def test_add_volatility_nday_signature_and_behavior():
    import inspect
    from src import feature_generator
    sig = inspect.signature(feature_generator.add_volatility_nday)
    assert list(sig.parameters.keys()) == ["df", "column", "window"]
    # This test only checks the function signature. Behavior, error handling, and logging are covered in dedicated test functions like test_add_volatility_nday_with_valid_inputs, test_add_volatility_nday_raises_appropriate_errors, and test_volatility_nday_logging.

def test_add_volatility_nday_with_valid_inputs():
    """Test add_volatility_nday function with various valid inputs."""
    from src.feature_generator import add_volatility_nday
    
    # Basic test case
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    result = add_volatility_nday(df, 'close', 2)
    # Use static pre-calculated expected values for independent verification
    expected = pd.Series([np.nan, np.nan, 0.6428243465332251, 0.5356869554443592, 0.45327357768369, 0.3885202094431676], 
                         name='volatility_2')
    pd.testing.assert_series_equal(result, expected)
      # Different column name
    df = pd.DataFrame({'price': [10, 11, 12, 13, 14, 15]})
    result = add_volatility_nday(df, 'price', 3)
    # Use static pre-calculated expected values
    expected = pd.Series([np.nan, np.nan, np.nan, 0.834480385952441, 0.700109607262632, 0.5958248258834902], 
                         name='volatility_3')
    pd.testing.assert_series_equal(result, expected)
    
    # Default parameters
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    result = add_volatility_nday(df)  # Should use 'close' as column and 20 as window
    # For window=20 with only 6 data points, all values should be NaN
    expected = pd.Series([np.nan] * 6, name='volatility_20')
    pd.testing.assert_series_equal(result, expected)

def test_add_volatility_nday_with_edge_cases():
    """Test add_volatility_nday function with edge cases."""
    from src.feature_generator import add_volatility_nday
    
    # Empty DataFrame
    df = pd.DataFrame({'close': []})
    result = add_volatility_nday(df)
    expected = pd.Series([], name='volatility_20', dtype='float64')
    pd.testing.assert_series_equal(result, expected)
    
    # DataFrame with NaNs not at the start
    df = pd.DataFrame({'close': [10, np.nan, 12, 13, np.nan, 15]})
    result = add_volatility_nday(df, window=2)
    # Use static pre-calculated expected values
    expected = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], name='volatility_2')
    pd.testing.assert_series_equal(result, expected)
    
    # DataFrame with mixed data types (but still numeric)
    df = pd.DataFrame({'close': [10, 11.5, 12, 13.7, 14, 15.2]})
    result = add_volatility_nday(df, window=3)
    # Use static pre-calculated expected values
    expected = pd.Series([np.nan, np.nan, np.nan, 5.924143874124078, 6.383736870366459, 5.992744287006658], 
                         name='volatility_3')
    pd.testing.assert_series_equal(result, expected)

def test_add_volatility_nday_raises_appropriate_errors():
    """Test add_volatility_nday function raises appropriate errors for invalid inputs."""
    from src.feature_generator import add_volatility_nday
    
    # Invalid DataFrame type
    with pytest.raises(ValueError, match="Input must be a pandas DataFrame"):
        add_volatility_nday("not_a_dataframe")
    
    # Non-existent column
    df = pd.DataFrame({'close': [10, 11, 12]})
    with pytest.raises(ValueError, match="Column 'not_a_column' not found"):
        add_volatility_nday(df, 'not_a_column')
    
    # Non-numeric column
    df = pd.DataFrame({'close': ['a', 'b', 'c']})
    with pytest.raises(ValueError, match="Column 'close' must be numeric"):
        add_volatility_nday(df)
    
    # Invalid window values
    df = pd.DataFrame({'close': [10, 11, 12]})
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        add_volatility_nday(df, window=0)
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        add_volatility_nday(df, window=-1)
    with pytest.raises(ValueError, match="Window size must be a positive integer"):
        add_volatility_nday(df, window="3")

def test_generate_features_exists():
    from src import feature_generator
    assert hasattr(feature_generator, "generate_features")

def test_generate_features_with_valid_configs():
    """Test generate_features function with various valid feature configurations."""
    from src.feature_generator import generate_features
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Test with single feature: SMA
    feature_config = {
        "sma": {"column": "close", "window": 3}
    }
    result = generate_features(df, feature_config)
    assert "sma_3" in result.columns
    assert list(result.columns) == ["close", "sma_3"]
    expected_sma = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3')
    pd.testing.assert_series_equal(result["sma_3"], expected_sma)
    
    # Test with single feature: price_change_pct_1d
    feature_config = {
        "price_change_pct_1d": {"column": "close"}
    }
    result = generate_features(df, feature_config)
    assert "price_change_pct_1d" in result.columns
    assert list(result.columns) == ["close", "price_change_pct_1d"]
    expected_pct = pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], 
                             name='price_change_pct_1d')
    pd.testing.assert_series_equal(result["price_change_pct_1d"], expected_pct)
    
    # Test with single feature: volatility_nday
    feature_config = {
        "volatility_nday": {"column": "close", "window": 2}
    }
    result = generate_features(df, feature_config)
    assert "volatility_2" in result.columns
    assert list(result.columns) == ["close", "volatility_2"]
    # Use static pre-calculated expected values
    expected_vol = pd.Series([np.nan, np.nan, 0.6428243465332251, 0.5356869554443592, 0.45327357768369, 0.3885202094431676], 
                             name='volatility_2')
    pd.testing.assert_series_equal(result["volatility_2"], expected_vol)

def test_generate_features_with_multiple_features():
    """Test generate_features function with multiple features in the configuration."""
    from src.feature_generator import generate_features
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Configuration with multiple features
    feature_config = {
        "sma": {"column": "close", "window": 3},
        "price_change_pct_1d": {"column": "close"},
        "volatility_nday": {"column": "close", "window": 2}
    }
    
    result = generate_features(df, feature_config)
    
    # Check that all feature columns are present
    assert "sma_3" in result.columns
    assert "price_change_pct_1d" in result.columns
    assert "volatility_2" in result.columns
    assert list(result.columns) == ["close", "sma_3", "price_change_pct_1d", "volatility_2"]
    
    # Verify each feature has correct values using static pre-calculated expected values
    expected_sma = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3')
    pd.testing.assert_series_equal(result["sma_3"], expected_sma)
    
    expected_pct = pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], 
                             name='price_change_pct_1d')
    pd.testing.assert_series_equal(result["price_change_pct_1d"], expected_pct)
    
    expected_vol = pd.Series([np.nan, np.nan, 0.6428243465332251, 0.5356869554443592, 0.45327357768369, 0.3885202094431676], 
                             name='volatility_2')
    pd.testing.assert_series_equal(result["volatility_2"], expected_vol)

def test_generate_features_with_multiple_sma_configurations():
    """Test generate_features function with multiple SMAs using the new configuration formats."""
    from src.feature_generator import generate_features
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Test with named feature instances (Case 1)
    feature_config = {
        "SMA_short": {"type": "sma", "column": "close", "window": 2},
        "SMA_long": {"type": "sma", "column": "close", "window": 3}
    }
    result = generate_features(df, feature_config)
    
    # Check that both SMA columns are present with correct names
    assert "SMA_short" in result.columns
    assert "SMA_long" in result.columns
    assert list(result.columns) == ["close", "SMA_short", "SMA_long"]
    
    # Verify values for short SMA
    expected_short_sma = pd.Series([np.nan, 10.5, 11.5, 12.5, 13.5, 14.5], name='SMA_short')
    pd.testing.assert_series_equal(result["SMA_short"], expected_short_sma)
    
    # Verify values for long SMA
    expected_long_sma = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='SMA_long')
    pd.testing.assert_series_equal(result["SMA_long"], expected_long_sma)
    
    # Test with feature type lists (Case 2)
    feature_config = {
        "smas": [
            {"name": "SMA_20", "column": "close", "window": 2},
            {"name": "SMA_50", "column": "close", "window": 3}
        ]
    }
    result = generate_features(df, feature_config)
    
    # Check that both SMA columns are present with correct names
    assert "SMA_20" in result.columns
    assert "SMA_50" in result.columns
    assert list(result.columns) == ["close", "SMA_20", "SMA_50"]
    
    # Verify values for SMA_20
    expected_sma_20 = pd.Series([np.nan, 10.5, 11.5, 12.5, 13.5, 14.5], name='SMA_20')
    pd.testing.assert_series_equal(result["SMA_20"], expected_sma_20)
    
    # Verify values for SMA_50
    expected_sma_50 = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='SMA_50')
    pd.testing.assert_series_equal(result["SMA_50"], expected_sma_50)
    
    # Test with mixed configuration (Case 1 + Case 3)
    feature_config = {
        "SMA_short": {"type": "sma", "column": "close", "window": 2},
        "volatility_nday": {"column": "close", "window": 2}
    }
    result = generate_features(df, feature_config)
    
    # Check that both columns are present with correct names
    assert "SMA_short" in result.columns
    assert "volatility_2" in result.columns
    assert list(result.columns) == ["close", "SMA_short", "volatility_2"]

def test_generate_features_with_legacy_config_and_new_format():
    """Test generate_features function with both legacy and new configuration formats."""
    from src.feature_generator import generate_features
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Configuration with both legacy and new formats
    feature_config = {
        "sma": {"column": "close", "window": 3},  # Legacy format
        "SMA_custom": {"type": "sma", "column": "close", "window": 2}  # New format
    }
    
    result = generate_features(df, feature_config)
    
    # Check that both SMA columns are present
    assert "sma_3" in result.columns
    assert "SMA_custom" in result.columns
    assert list(result.columns) == ["close", "sma_3", "SMA_custom"]
    
    # Verify values for legacy SMA
    expected_sma_3 = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3')
    pd.testing.assert_series_equal(result["sma_3"], expected_sma_3)
    
    # Verify values for custom named SMA
    expected_sma_custom = pd.Series([np.nan, 10.5, 11.5, 12.5, 13.5, 14.5], name='SMA_custom')
    pd.testing.assert_series_equal(result["SMA_custom"], expected_sma_custom)

def test_generate_features_missing_name_in_list_config(caplog):
    """Test generate_features function with missing name in list configuration."""
    from src.feature_generator import generate_features
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Configuration with missing name in list
    feature_config = {
        "smas": [
            {"name": "SMA_20", "column": "close", "window": 2},
            {"column": "close", "window": 3}  # Missing name
        ]
    }
    
    with caplog.at_level(logging.WARNING):
        result = generate_features(df, feature_config)
    
    # Only the first SMA should be added
    assert "SMA_20" in result.columns
    assert list(result.columns) == ["close", "SMA_20"]
    
    # Verify warning log
    assert any("Missing 'name' in a sma configuration" in record.getMessage() for record in caplog.records)

def test_generate_features_parameter_passing():
    """Test generate_features correctly passes parameters to underlying functions."""
    from src.feature_generator import generate_features
    from unittest.mock import patch, ANY
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Configuration with different parameters for features
    feature_config = {
        "sma": {"column": "close", "window": 5},
        "price_change_pct_1d": {"column": "close"},
        "volatility_nday": {"column": "close", "window": 3}
    }
    
    # Mock the underlying feature functions to verify parameter passing
    with patch('src.feature_generator.add_sma') as mock_add_sma, \
         patch('src.feature_generator.add_price_change_pct_1d') as mock_add_price_change, \
         patch('src.feature_generator.add_volatility_nday') as mock_add_volatility:
        
        # Set up the mocks to return a dummy Series
        mock_add_sma.return_value = pd.Series([1, 2, 3, 4, 5, 6], name='sma_5')
        mock_add_price_change.return_value = pd.Series([1, 2, 3, 4, 5, 6], name='price_change_pct_1d')
        mock_add_volatility.return_value = pd.Series([1, 2, 3, 4, 5, 6], name='volatility_3')
        
        # Call the function
        generate_features(df, feature_config)
        
        # Verify that the functions were called with the correct parameters
        # Using ANY matcher for the DataFrame to avoid comparison issues
        mock_add_sma.assert_called_once()
        assert mock_add_sma.call_args[1]['column'] == "close"
        assert mock_add_sma.call_args[1]['window'] == 5
        
        mock_add_price_change.assert_called_once()
        assert mock_add_price_change.call_args[1]['column'] == "close"
        
        mock_add_volatility.assert_called_once()
        assert mock_add_volatility.call_args[1]['column'] == "close"
        assert mock_add_volatility.call_args[1]['window'] == 3

def test_generate_features_with_price_changes_volatility_metrics_lists():
    """Test generate_features function with other predefined list keys."""
    from src.feature_generator import generate_features
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Test with price_changes list key
    feature_config = {
        "price_changes": [
            {"name": "Daily_Change", "column": "close"}
        ]
    }
    result = generate_features(df, feature_config)
    
    # Check that price change column is present with correct name
    assert "Daily_Change" in result.columns
    assert list(result.columns) == ["close", "Daily_Change"]
    
    # Expected values for Daily_Change (same as price_change_pct_1d but with custom name)
    expected_pct = pd.Series([np.nan, 10.0, 9.090909090909092, 8.333333333333332, 7.6923076923076925, 7.142857142857142], 
                             name='Daily_Change')
    pd.testing.assert_series_equal(result["Daily_Change"], expected_pct)
    
    # Test with volatility_metrics list key
    feature_config = {
        "volatility_metrics": [
            {"name": "Vol_10", "column": "close", "window": 2}
        ]
    }
    result = generate_features(df, feature_config)
    
    # Check that volatility column is present with correct name
    assert "Vol_10" in result.columns
    assert list(result.columns) == ["close", "Vol_10"]
    
    # Expected values for Vol_10 (same as volatility_2 but with custom name)
    expected_vol = pd.Series([np.nan, np.nan, 0.6428243465332251, 0.5356869554443592, 0.45327357768369, 0.3885202094431676], 
                             name='Vol_10')
    pd.testing.assert_series_equal(result["Vol_10"], expected_vol)
    
    # Test with multiple predefined list keys
    feature_config = {
        "smas": [
            {"name": "SMA_Short", "column": "close", "window": 2}
        ],
        "price_changes": [
            {"name": "Daily_Change", "column": "close"}
        ],
        "volatility_metrics": [
            {"name": "Vol_10", "column": "close", "window": 2}
        ]
    }
    result = generate_features(df, feature_config)
    
    # Check that all columns are present with correct names
    assert "SMA_Short" in result.columns
    assert "Daily_Change" in result.columns
    assert "Vol_10" in result.columns
    assert list(result.columns) == ["close", "SMA_Short", "Daily_Change", "Vol_10"]

def test_generate_features_ignores_invalid_list_keys(caplog):
    """Test generate_features ignores list configurations with invalid keys."""
    from src.feature_generator import generate_features
    import logging
    
    # Basic DataFrame
    df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
    
    # Test with invalid list key 'invalid_features'
    feature_config = {
        "invalid_features": [
            {"name": "Some_Feature", "column": "close", "window": 2}
        ],
        "SMA_valid": {"type": "sma", "column": "close", "window": 2}  # This should still work
    }
    
    # The invalid list key should be ignored with a warning
    with caplog.at_level(logging.WARNING):
        result = generate_features(df, feature_config)
    
    # Check that only the valid feature was added
    assert "SMA_valid" in result.columns
    assert "Some_Feature" not in result.columns
    assert list(result.columns) == ["close", "SMA_valid"]
    
    # Verify warning log about unrecognized list key
    assert any("Unrecognized list configuration key 'invalid_features'" in record.getMessage() for record in caplog.records)

def test_feature_conflict_resolution(caplog):
    """Test that the feature generator correctly handles column name conflicts."""
    from src.feature_generator import generate_features, add_sma
    import logging
    
    # Create a DataFrame with an existing 'sma_3' column
    df = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15],
        'sma_3': [100, 101, 102, 103, 104, 105]  # This is an existing column with the same name
    })
    
    # Test Case 1: Legacy format with conflicting feature
    feature_config = {
        "sma": {"column": "close", "window": 3}
    }
    
    with caplog.at_level(logging.WARNING):
        result = generate_features(df, feature_config)
    
    # Verify that the original column is preserved
    assert "sma_3" in result.columns
    assert list(result["sma_3"]) == [100, 101, 102, 103, 104, 105]
    
    # Verify that the new column was renamed to avoid conflict
    assert "sma_3_1" in result.columns
    expected_sma = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0], name='sma_3_1')
    pd.testing.assert_series_equal(result["sma_3_1"], expected_sma)
    
    # Verify warning about column conflict
    assert any("Column 'sma_3' already exists in DataFrame" in record.getMessage() for record in caplog.records)
    
    # Test Case 2: Named feature instance with conflicting name
    df = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15],
        'SMA_custom': [100, 101, 102, 103, 104, 105]  # This is an existing column with the same name
    })
    
    feature_config = {
        "SMA_custom": {"type": "sma", "column": "close", "window": 2}
    }
    
    with caplog.at_level(logging.WARNING):
        result = generate_features(df, feature_config)
    
    # Verify that the original column is preserved
    assert "SMA_custom" in result.columns
    assert list(result["SMA_custom"]) == [100, 101, 102, 103, 104, 105]
    
    # Verify that the new column was renamed to avoid conflict
    assert "SMA_custom_1" in result.columns
    expected_sma_custom = pd.Series([np.nan, 10.5, 11.5, 12.5, 13.5, 14.5], name='SMA_custom_1')
    pd.testing.assert_series_equal(result["SMA_custom_1"], expected_sma_custom)
    
    # Test Case 3: Multiple conflicts requiring different suffixes
    df = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15],
        'sma_2': [100, 101, 102, 103, 104, 105],
        'sma_2_1': [200, 201, 202, 203, 204, 205]
    })
    
    feature_config = {
        "sma": {"column": "close", "window": 2}
    }
    
    with caplog.at_level(logging.WARNING):
        result = generate_features(df, feature_config)
    
    # Verify that the original columns are preserved
    assert "sma_2" in result.columns
    assert "sma_2_1" in result.columns
    assert list(result["sma_2"]) == [100, 101, 102, 103, 104, 105]
    assert list(result["sma_2_1"]) == [200, 201, 202, 203, 204, 205]
    
    # Verify that the new column was renamed with suffix _2
    assert "sma_2_2" in result.columns
    expected_sma_2_2 = pd.Series([np.nan, 10.5, 11.5, 12.5, 13.5, 14.5], name='sma_2_2')
    pd.testing.assert_series_equal(result["sma_2_2"], expected_sma_2_2)
