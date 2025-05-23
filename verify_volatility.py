import pandas as pd
import numpy as np

# Create the test dataframe
df = pd.DataFrame({'close': [10, 11.5, 12, 13.7, 14, 15.2]})

# Calculate price changes
price_change = (df['close'] - df['close'].shift(1)) / df['close'].shift(1) * 100
print("Price changes:")
print(price_change)

# Calculate volatility with window=3
volatility = price_change.rolling(window=3, min_periods=3).std(ddof=1)
print("\nVolatility (window=3):")
print(volatility)

# Print the specific value at index 3
print(f"\nValue at index 3: {volatility.iloc[3]}")
