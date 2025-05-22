import pandas as pd
import numpy as np
import pytest
import logging
from src.strategies import generate_sma_crossover_signals, apply_strategy

def test_apply_strategy_with_sma_crossover():
    """Test apply_strategy function with SMA crossover strategy."""
    # Create test data with known crossover points
    dates = pd.date_range(start='2023-01-01', periods=10)
    test_data = pd.DataFrame({
        'Close': [100, 102, 104, 103, 101, 99, 97, 99, 102, 105],
        'Volume': [1000] * 10
    }, index=dates)
      # Add SMAs to test data (ensure crossovers)
    test_data['SMA5'] = [np.nan, 100, 101, 102, 103, 104, 103, 102, 101, 100]
    test_data['SMA10'] = [np.nan, 101, 101, 101, 102, 103, 103, 101, 102, 103]
    # Crossover points:
    # - At index 3: SMA5 crosses above SMA10 (buy)
    # - At index 8: SMA5 crosses below SMA10 (sell)
    
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA5',
            'slow_sma': 'SMA10'
        }
    }
    
    # Apply strategy
    result_df = apply_strategy(test_data, strategy_params)
    
    # Assertions
    assert 'signal' in result_df.columns
    assert result_df['signal'].iloc[3] == 1  # Buy signal when fast crosses above slow
    assert result_df['signal'].iloc[8] == -1  # Sell signal when fast crosses below slow
    assert result_df['signal'].iloc[5] == 0  # No signal during most periods
    assert result_df['signal'].isna().sum() == 0  # No NaN values in signal column

def test_apply_strategy_invalid_type():
    """Test apply_strategy with invalid strategy type."""
    # Test with invalid strategy type
    test_data = pd.DataFrame({'Close': [100, 102, 104]})
    strategy_params = {
        'strategy_type': 'invalid_strategy',
        'parameters': {}
    }
    
    with pytest.raises(ValueError, match="Unsupported strategy type"):
        apply_strategy(test_data, strategy_params)

def test_apply_strategy_missing_parameters():
    """Test apply_strategy with missing required parameters."""
    # Test with missing required parameters
    test_data = pd.DataFrame({'Close': [100, 102, 104]})
    test_data['SMA5'] = [100, 101, 102]
    test_data['SMA10'] = [99, 100, 101]
    
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            # Missing fast_sma parameter
            'slow_sma': 'SMA10'
        }
    }
    
    with pytest.raises(ValueError, match="Missing required parameter"):
        apply_strategy(test_data, strategy_params)
        
    # Test with missing slow_sma parameter
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA5',
            # Missing slow_sma parameter
        }
    }
    
    with pytest.raises(ValueError, match="Missing required parameter"):
        apply_strategy(test_data, strategy_params)

def test_apply_strategy_different_column_names():
    """Test apply_strategy with different column names for fast and slow SMAs."""
    # Create test data with custom column names
    dates = pd.date_range(start='2023-01-01', periods=10)
    test_data = pd.DataFrame({
        'Close': [100, 102, 104, 103, 101, 99, 97, 99, 102, 105],
        'Custom_Fast': [np.nan, 100, 101, 102, 103, 104, 103, 102, 101, 100],
        'Custom_Slow': [np.nan, 101, 101, 101, 102, 103, 103, 101, 102, 103]
    }, index=dates)
    
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'Custom_Fast',
            'slow_sma': 'Custom_Slow'
        }
    }
    
    # Apply strategy
    result_df = apply_strategy(test_data, strategy_params)
    
    # Assertions
    assert 'signal' in result_df.columns
    assert result_df['signal'].iloc[3] == 1  # Buy signal when fast crosses above slow
    assert result_df['signal'].iloc[8] == -1  # Sell signal when fast crosses below slow
    assert result_df['signal'].iloc[5] == 0  # No signal during most periods

def test_apply_strategy_empty_dataframe():
    """Test apply_strategy with an empty DataFrame."""
    # Create an empty DataFrame
    test_data = pd.DataFrame(columns=['Close', 'SMA5', 'SMA10'])
    
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA5',
            'slow_sma': 'SMA10'
        }
    }
    
    # Apply strategy to empty DataFrame
    result_df = apply_strategy(test_data, strategy_params)
    
    # Assertions
    assert 'signal' in result_df.columns
    assert len(result_df) == 0  # Result should still be empty

def test_apply_strategy_with_nans():
    """Test apply_strategy with NaNs in feature columns."""
    # Create test data with NaNs
    dates = pd.date_range(start='2023-01-01', periods=10)
    test_data = pd.DataFrame({
        'Close': [100, 102, 104, 103, 101, 99, 97, 99, 102, 105],
        'SMA5': [np.nan, 100, np.nan, 102, 103, 104, np.nan, 102, 101, 100],
        'SMA10': [np.nan, 101, 101, np.nan, 102, 103, 103, np.nan, 102, 103]
    }, index=dates)
    
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA5',
            'slow_sma': 'SMA10'
        }
    }
    
    # Apply strategy
    result_df = apply_strategy(test_data, strategy_params)
    
    # Assertions
    assert 'signal' in result_df.columns
    # NaN locations should have signal=0 (no signal)
    assert result_df['signal'].iloc[0] == 0  # NaN in both SMA columns
    assert result_df['signal'].iloc[2] == 0  # NaN in fast SMA
    assert result_df['signal'].iloc[3] == 0  # NaN in slow SMA
    assert result_df['signal'].iloc[6] == 0  # NaN in fast SMA
    assert result_df['signal'].iloc[7] == 0  # NaN in slow SMA

def test_apply_strategy_logging(caplog):
    """Test that apply_strategy logs the expected messages."""
    # Set up logging
    caplog.set_level(logging.INFO)
    
    # Create test data
    test_data = pd.DataFrame({
        'Close': [100, 102, 104],
        'SMA5': [100, 101, 102],
        'SMA10': [99, 100, 101]
    })
    
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA5',
            'slow_sma': 'SMA10'
        }
    }
    
    # Apply strategy
    result_df = apply_strategy(test_data, strategy_params)
    
    # Assertions for logging
    assert "Applying sma_crossover strategy" in caplog.text
    assert "Strategy applied, generated" in caplog.text

def test_apply_strategy_preserves_original_df():
    """Test that apply_strategy doesn't modify the original DataFrame."""
    # Create test data
    test_data = pd.DataFrame({
        'Close': [100, 102, 104],
        'SMA5': [100, 101, 102],
        'SMA10': [99, 100, 101]
    })
    
    # Make a copy to compare later
    original_df = test_data.copy()
    
    strategy_params = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA5',
            'slow_sma': 'SMA10'
        }
    }
    
    # Apply strategy
    result_df = apply_strategy(test_data, strategy_params)
    
    # Assertions
    assert 'signal' in result_df.columns
    assert 'signal' not in test_data.columns  # Original shouldn't be modified
    pd.testing.assert_frame_equal(test_data, original_df)  # Original should be unchanged
