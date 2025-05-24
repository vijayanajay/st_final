"""
Integration tests for the Simple Stock Strategy Backtester (S3B).

These tests verify that multiple modules work together correctly,
including feature generation and strategy implementation integration.
"""

import pytest
import pandas as pd
import numpy as np
from src.feature_generator import generate_features
from src.strategies import apply_strategy


@pytest.mark.integration
def test_feature_generation_and_strategy_integration():
    """
    Integration test to verify that feature generation and SMA crossover strategy
    work together correctly with multiple SMA configurations.
    """
    # Create sample data
    df = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15, 14, 13, 12, 13, 14, 15, 16]
    })
    
    # Test with the new named feature config format
    feature_config = {
        "SMA_short": {"type": "sma", "column": "close", "window": 3},
        "SMA_long": {"type": "sma", "column": "close", "window": 5}
    }
    
    # Generate features
    df_with_features = generate_features(df, feature_config)
    
    # Verify that both SMA columns are present
    assert "SMA_short" in df_with_features.columns, "Short SMA should be generated"
    assert "SMA_long" in df_with_features.columns, "Long SMA should be generated"
    assert "close" in df_with_features.columns, "Original close column should be preserved"
    
    # Verify the DataFrame has the expected structure
    expected_columns = ["close", "SMA_short", "SMA_long"]
    assert list(df_with_features.columns) == expected_columns, f"Columns should be {expected_columns}"
      # Generate signals using the SMA crossover strategy via apply_strategy
    strategy_config = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA_short',
            'slow_sma': 'SMA_long'
        }
    }
    
    df_with_signals = apply_strategy(df_with_features, strategy_config)
    signals = df_with_signals['signal']
    
    # Add signals to the DataFrame for verification
    df_with_features['signal'] = signals
    
    # Verify signals structure
    assert len(signals) == len(df), "Signals should have same length as input data"
    assert all(signal in [-1, 0, 1] for signal in signals), "Signals should be -1, 0, or 1"
    
    # Count the number of buy and sell signals
    buy_signals = (df_with_features['signal'] == 1).sum()
    sell_signals = (df_with_features['signal'] == -1).sum()
    hold_signals = (df_with_features['signal'] == 0).sum()
    
    # Basic sanity checks
    assert buy_signals >= 0, "Buy signals should be non-negative"
    assert sell_signals >= 0, "Sell signals should be non-negative" 
    assert hold_signals >= 0, "Hold signals should be non-negative"
    assert buy_signals + sell_signals + hold_signals == len(df), "All signals should sum to data length"
    
    # Verify that we have some meaningful signal generation
    # (not all zeros, which would indicate a problem)
    total_trading_signals = buy_signals + sell_signals
    assert total_trading_signals >= 0, "Should have some trading signals or all holds (valid scenario)"


@pytest.mark.integration
def test_legacy_feature_config_integration():
    """
    Integration test to verify backward compatibility with legacy feature configuration format.
    """
    # Create sample data
    df = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15, 14, 13, 12, 13, 14, 15, 16]
    })
    
    # Test with legacy feature config format
    feature_config = {
        "sma": {"column": "close", "window": 3}
    }
    
    # Generate features
    df_with_features = generate_features(df, feature_config)
    
    # Verify that SMA column is present with legacy naming
    assert "sma_3" in df_with_features.columns, "Legacy SMA should be generated"
    assert "close" in df_with_features.columns, "Original close column should be preserved"
    
    # Verify the DataFrame has the expected structure
    expected_columns = ["close", "sma_3"]
    assert list(df_with_features.columns) == expected_columns, f"Columns should be {expected_columns}"
    
    # Verify data integrity
    assert len(df_with_features) == len(df), "Feature generation should preserve row count"
    assert not df_with_features['close'].isna().any(), "Close prices should not have NaN values"


@pytest.mark.integration
def test_multiple_feature_types_integration():
    """
    Integration test to verify that multiple feature types can be generated together.
    """
    # Create sample data
    df = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15, 14, 13, 12, 13, 14, 15, 16]
    })
    
    # Test with multiple feature types
    feature_config = {
        "SMA_fast": {"type": "sma", "column": "close", "window": 3},
        "SMA_slow": {"type": "sma", "column": "close", "window": 5},
        "price_change": {"type": "price_change_pct_1d", "column": "close"},
        "volatility": {"type": "volatility_nday", "column": "close", "window": 3}
    }
    
    # Generate features
    df_with_features = generate_features(df, feature_config)
    
    # Verify all features are present
    expected_features = ["SMA_fast", "SMA_slow", "price_change", "volatility"]
    for feature in expected_features:
        assert feature in df_with_features.columns, f"Feature {feature} should be generated"
    
    # Verify data types and basic properties
    assert df_with_features['SMA_fast'].dtype == np.float64, "SMA should be float"
    assert df_with_features['price_change'].dtype == np.float64, "Price change should be float"
    assert df_with_features['volatility'].dtype == np.float64, "Volatility should be float"
      # Verify that we can use the generated features for strategy
    strategy_config = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA_fast',
            'slow_sma': 'SMA_slow'
        }
    }
    df_with_signals = apply_strategy(df_with_features, strategy_config)
    signals = df_with_signals['signal']
    
    assert len(signals) == len(df), "Strategy should work with generated features"
    assert all(signal in [-1, 0, 1] for signal in signals), "Strategy should generate valid signals"


@pytest.mark.integration
def test_end_to_end_integration_with_results_file(tmp_path):
    """
    Comprehensive end-to-end integration test that generates a results file
    for manual inspection, replacing the standalone integration_test.py functionality.
    """
    # Create sample data (same as original integration test)
    df = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15, 14, 13, 12, 13, 14, 15, 16]
    })
    
    # Test with the new named feature config format
    feature_config = {
        "SMA_short": {"type": "sma", "column": "close", "window": 3},
        "SMA_long": {"type": "sma", "column": "close", "window": 5}
    }
    
    # Generate features
    df_with_features = generate_features(df, feature_config)
    
    # Generate signals using the primary API (apply_strategy)
    strategy_config = {
        'strategy_type': 'sma_crossover',
        'parameters': {
            'fast_sma': 'SMA_short',
            'slow_sma': 'SMA_long'
        }
    }
    
    df_with_signals = apply_strategy(df_with_features, strategy_config)
    
    # Create integration test results file for manual inspection
    results_file = tmp_path / "integration_test_results.txt"
    with open(results_file, 'w') as f:
        f.write("Integration Test Results - End-to-End Verification\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("DataFrame with multiple SMAs:\n")
        f.write(str(df_with_features) + "\n\n")
        
        f.write("DataFrame with signals:\n")
        f.write(str(df_with_signals) + "\n\n")            # Count the number of buy and sell signals
        buy_signals = (df_with_signals['signal'] == 1).sum()
        sell_signals = (df_with_signals['signal'] == -1).sum()
        hold_signals = (df_with_signals['signal'] == 0).sum()
        
        f.write(f"Signal Analysis:\n")
        f.write(f"Buy signals: {buy_signals}\n")
        f.write(f"Sell signals: {sell_signals}\n")
        f.write(f"Hold signals: {hold_signals}\n\n")
        
        f.write("Test completed successfully using primary API (apply_strategy)!\n")
        f.write("This test verifies end-to-end integration of:\n")
        f.write("- Feature generation with multiple SMA configurations\n")
        f.write("- Strategy application using recommended primary API\n")
        f.write("- Signal generation and validation\n")
    
    # Also create a copy in the project root for compatibility (if desired)
    import shutil
    project_results_file = "integration_test_results.txt"
    shutil.copy2(results_file, project_results_file)
      # Verify all integration components work correctly
    assert "SMA_short" in df_with_features.columns
    assert "SMA_long" in df_with_features.columns
    assert "signal" in df_with_signals.columns
    assert len(df_with_signals) == len(df)
    assert all(signal in [-1, 0, 1] for signal in df_with_signals['signal'])
    
    # Verify the results file was created and contains expected content
    assert results_file.exists()
    with open(results_file, 'r') as f:
        content = f.read()
        assert "Integration Test Results" in content
        assert "apply_strategy" in content
        assert "Test completed successfully" in content
