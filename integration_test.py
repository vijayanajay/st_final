"""
Integration test script to verify that the fixed feature_generator.py can generate multiple SMAs
and use them with the SMA crossover strategy.
"""

import pandas as pd
import numpy as np
from src.feature_generator import generate_features
from src.strategies import generate_sma_crossover_signals

def test_integration():
    # Create a log file
    with open('integration_test_results.txt', 'w') as f:
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
        f.write("DataFrame with multiple SMAs:\n")
        f.write(str(df_with_features) + "\n\n")
        
        # Verify that both SMA columns are present
        assert "SMA_short" in df_with_features.columns
        assert "SMA_long" in df_with_features.columns
        
        # Generate signals using the SMA crossover strategy
        signals = generate_sma_crossover_signals(df_with_features)
        
        # Add signals to the DataFrame for visualization
        df_with_features['signal'] = signals
        
        f.write("DataFrame with signals:\n")
        f.write(str(df_with_features) + "\n\n")
        
        # Count the number of buy and sell signals
        buy_signals = (df_with_features['signal'] == 1).sum()
        sell_signals = (df_with_features['signal'] == -1).sum()
        
        f.write(f"Buy signals: {buy_signals}\n")
        f.write(f"Sell signals: {sell_signals}\n\n")
        
        f.write("Test completed successfully!\n")
    
    print("Integration test completed. Results written to integration_test_results.txt")

if __name__ == "__main__":
    test_integration()
