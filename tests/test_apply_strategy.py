import pandas as pd
import numpy as np
import pytest
from src.strategies import generate_sma_crossover_signals, apply_strategy

def test_apply_strategy_with_sma_crossover():
    """Test apply_strategy function with SMA crossover strategy."""
    # Create test data with known crossover points
    dates = pd.date_range(start='2023-01-01', periods=10)
    test_data = pd.DataFrame({
        'Close': [100, 102, 104, 103, 101, 99, 97, 99, 102, 105],
        'Volume': [1000] * 10
    }, index=dates)
    
    # Add SMAs to test data
    test_data['SMA5'] = [np.nan, np.nan, np.nan, np.nan, 102, 101.8, 100.8, 99.8, 99.6, 100.4]
    test_data['SMA10'] = [np.nan] * 10
    
    # Define strategy parameters
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
# Assertions
# Assertions
assert 'signal' in result_df.columns
assert result_df['signal'].iloc[8] == 1  # Buy signal when fast crosses above slow
assert result_df['signal'].iloc[9] == -1  # Sell signal when fast crosses below slow
assert result_df['signal'].iloc[6] == 0  # No signal during most periods
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
