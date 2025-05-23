# tests/test_strategy_pattern.py
"""
Tests for the Strategy pattern implementation in src.strategies module.
"""

import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_series_equal
from src.strategies import BaseStrategy, SMACrossoverStrategy, STRATEGY_REGISTRY, apply_strategy


def test_strategy_registry():
    """Test that the strategy registry contains expected strategies."""
    assert 'sma_crossover' in STRATEGY_REGISTRY
    assert STRATEGY_REGISTRY['sma_crossover'] == SMACrossoverStrategy


def test_sma_crossover_strategy_required_params():
    """Test that SMACrossoverStrategy returns the expected required parameters."""
    strategy = SMACrossoverStrategy()
    required_params = strategy.get_required_parameters()
    assert required_params == ['fast_sma', 'slow_sma']


def test_sma_crossover_strategy_validate_parameters():
    """Test parameter validation in SMACrossoverStrategy."""
    strategy = SMACrossoverStrategy()
    
    # Valid parameters
    valid_params = {'fast_sma': 'SMA5', 'slow_sma': 'SMA10'}
    try:
        strategy.validate_parameters(valid_params)
    except ValueError:
        pytest.fail("validate_parameters raised ValueError unexpectedly with valid parameters")
    
    # Missing parameter
    missing_params = {'fast_sma': 'SMA5'}
    with pytest.raises(ValueError, match="Missing required parameter 'slow_sma'"):
        strategy.validate_parameters(missing_params)


def test_sma_crossover_strategy_generate_signals():
    """Test SMACrossoverStrategy.generate_signals produces correct signals."""
    strategy = SMACrossoverStrategy()
    
    # Create test data with known crossover points
    data = {
        'close': [10, 12, 13, 15, 14, 13, 12, 11, 13, 15],
        'SMA5': [10, 11, 12, 13.5, 14, 13.5, 13, 12, 12.5, 14],
        'SMA10': [10, 10.5, 11, 11.5, 12.5, 13, 13.5, 13, 12.5, 12.5]
    }
    df = pd.DataFrame(data)
    
    params = {'fast_sma': 'SMA5', 'slow_sma': 'SMA10'}
    
    # Period 0: SMA5=10, SMA10=10. Prev_short=NaN, Prev_long=NaN. Signal: 0 (HOLD)
    # Period 1: SMA5=11, SMA10=10.5. Prev_short=10, Prev_long=10. (10 <= 10) and (11 > 10.5) => BUY (1)
    # Period 2: SMA5=12, SMA10=11. Prev_short=11, Prev_long=10.5. (11 > 10.5) and (12 > 11) => HOLD (0)
    # Period 3: SMA5=13.5, SMA10=11.5. Prev_short=12, Prev_long=11. (12 > 11) and (13.5 > 11.5) => HOLD (0)
    # Period 4: SMA5=14, SMA10=12.5. Prev_short=13.5, Prev_long=11.5. (13.5 > 11.5) and (14 > 12.5) => HOLD (0)
    # Period 5: SMA5=13.5, SMA10=13. Prev_short=14, Prev_long=12.5. (14 > 12.5) and (13.5 > 13) => HOLD (0)
    # Period 6: SMA5=13, SMA10=13.5. Prev_short=13.5, Prev_long=13. (13.5 > 13) and (13 < 13.5) => SELL (-1)
    # Period 7: SMA5=12, SMA10=13. Prev_short=13, Prev_long=13.5. (13 < 13.5) and (12 < 13) => HOLD (0)
    # Period 8: SMA5=12.5, SMA10=12.5. Prev_short=12, Prev_long=13. (12 < 13) and (12.5 == 12.5) => HOLD (0)
    # Period 9: SMA5=14, SMA10=12.5. Prev_short=12.5, Prev_long=12.5. (12.5 == 12.5) and (14 > 12.5) => BUY (1)
    
    expected_signals = pd.Series([0, 1, 0, 0, 0, 0, -1, 0, 0, 1], name="signal")
    
    actual_signals = strategy.generate_signals(df, params)
    
    assert_series_equal(actual_signals, expected_signals, check_dtype=False)


def test_sma_crossover_strategy_missing_columns():
    """Test SMACrossoverStrategy with missing columns."""
    strategy = SMACrossoverStrategy()
    
    # Create test data with missing columns
    df = pd.DataFrame({'close': [10, 12, 13]})
    params = {'fast_sma': 'SMA5', 'slow_sma': 'SMA10'}
    
    with pytest.raises(ValueError, match="Input DataFrame must contain"):
        strategy.generate_signals(df, params)


def test_apply_strategy_with_new_implementation():
    """Test apply_strategy with the new Strategy pattern implementation."""
    # Create test data with known crossover points
    dates = pd.date_range(start='2023-01-01', periods=10)
    test_data = pd.DataFrame({
        'Close': [100, 102, 104, 103, 101, 99, 97, 99, 102, 105],
        'Volume': [1000] * 10
    }, index=dates)
    # Add SMAs to test data (ensure crossovers)
    test_data['SMA5'] = [np.nan, 100, 101, 102, 103, 104, 103, 102, 101, 100]
    test_data['SMA10'] = [np.nan, 101, 101, 101, 102, 103, 103, 101, 102, 103]
    
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
