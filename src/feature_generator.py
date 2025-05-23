import pandas as pd
import logging

def add_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
    """
    Add Simple Moving Average (SMA) to the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing price data.
        column (str): Name of the column to calculate SMA on.
        window (int): Window size for the moving average. Must be > 0.

    Returns:
        pd.Series: Series containing the SMA values, named as 'sma_{window}'.

    Raises:
        ValueError: If the column does not exist or window is invalid.
    """
    if not isinstance(df, pd.DataFrame):
        logging.error("Input must be a pandas DataFrame.")
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        logging.error(f"Column '{column}' not found in DataFrame.")
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        logging.error(f"Column '{column}' must be numeric for SMA calculation.")
        raise ValueError(f"Column '{column}' must be numeric for SMA calculation.")
    if not isinstance(window, int) or window <= 0:
        logging.error("Window size must be a positive integer.")
        raise ValueError("Window size must be a positive integer.")

    logging.info(f"Calculating SMA: column={column}, window={window}")
    sma = df[column].rolling(window=window, min_periods=window).mean()
    sma.name = f'sma_{window}'
    return sma

def add_price_change_pct_1d(df: pd.DataFrame, column: str = "close") -> pd.Series:
    """
    Add 1-day price change percentage to the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing price data.
        column (str): Name of the column to calculate price change percentage on. Defaults to 'close'.

    Returns:
        pd.Series: Series containing the 1-day price change percentage, named as 'price_change_pct_1d'.

    Raises:
        ValueError: If the column does not exist or is not numeric.
    """
    if not isinstance(df, pd.DataFrame):
        logging.error("Input must be a pandas DataFrame.")
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        logging.error(f"Column '{column}' not found in DataFrame.")
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        logging.error(f"Column '{column}' must be numeric.")
        raise ValueError(f"Column '{column}' must be numeric.")
    logging.info(f"Calculating 1-day price change percentage: column={column}")
    pct = (df[column] - df[column].shift(1)) / df[column].shift(1) * 100
    pct.name = 'price_change_pct_1d'
    return pct

def add_volatility_nday(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series:
    """
    Add n-day rolling volatility to the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing price data.
        column (str): Name of the column to calculate volatility on. Defaults to 'close'.
        window (int): Window size for the rolling standard deviation. Must be > 0.

    Returns:
        pd.Series: Series containing the rolling volatility, named as 'volatility_{window}'.

    Raises:
        ValueError: If the column does not exist, is not numeric, or window is invalid.
    """
    if not isinstance(df, pd.DataFrame):
        logging.error("Input must be a pandas DataFrame.")
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        logging.error(f"Column '{column}' not found in DataFrame.")
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        logging.error(f"Column '{column}' must be numeric.")
        raise ValueError(f"Column '{column}' must be numeric.")
    if not isinstance(window, int) or window <= 0:
        logging.error("Window size must be a positive integer.")
        raise ValueError("Window size must be a positive integer.")
    logging.info(f"Calculating volatility: column={column}, window={window}")
    price_change = (df[column] - df[column].shift(1)) / df[column].shift(1) * 100
    volatility = price_change.rolling(window=window, min_periods=window).std()
    volatility.name = f'volatility_{window}'
    return volatility

# Backward compatibility aliases for tests
def calculate_sma(df: pd.DataFrame, column: str, window: int) -> pd.Series:
    """
    This is an alias for add_sma provided for backward compatibility with tests.
    
    See add_sma for full documentation.
    """
    return add_sma(df, column, window)

def calculate_price_change_pct(df: pd.DataFrame, column: str = "close") -> pd.Series:
    """
    This is an alias for add_price_change_pct_1d provided for backward compatibility with tests.
    
    See add_price_change_pct_1d for full documentation.
    """
    return add_price_change_pct_1d(df, column)

def calculate_volatility(df: pd.DataFrame, column: str = "close", window: int = 20) -> pd.Series:
    """
    This is an alias for add_volatility_nday provided for backward compatibility with tests.
    
    See add_volatility_nday for full documentation.
    """
    return add_volatility_nday(df, column, window)

def generate_features(df: pd.DataFrame, feature_config: dict) -> pd.DataFrame:
    """
    Orchestrator to generate all features as specified in feature_config.

    Args:
        df (pd.DataFrame): Input DataFrame.
        feature_config (dict): Dict specifying which features to add and their parameters.
            The config can be structured in three ways:
            1. Using feature names as keys for named instances:
                {
                    "SMA_short": {"type": "sma", "column": "close", "window": 20},
                    "SMA_long": {"type": "sma", "column": "close", "window": 50},
                    ...
                }
            2. Using predefined list keys for multiple configurations of the same feature type:
                {
                    "smas": [
                        {"name": "SMA_short", "column": "close", "window": 20},
                        {"name": "SMA_long", "column": "close", "window": 50}
                    ],
                    ...
                }
                Valid list keys are: "smas", "price_changes", "volatility_metrics"
            3. Legacy format (for backward compatibility):
                {
                    "sma": {"column": "close", "window": 20},
                    "price_change_pct_1d": {"column": "close"},
                    "volatility_nday": {"column": "close", "window": 20}
                }

    Returns:
        pd.DataFrame: DataFrame with new feature columns added.
    """
    # Create a working copy of the DataFrame
    result_df = df.copy()
      # Define known feature types that can be used in list-based configurations
    list_feature_mappings = {
        'smas': 'sma',
        'price_changes': 'price_change_pct_1d',
        'volatility_metrics': 'volatility_nday',
        # Add more mappings as needed for future feature types
    }
    
    for feature_key, config in feature_config.items():
        # Case 1: Named feature instance with a 'type' field
        if isinstance(config, dict) and 'type' in config:
            feature_type = config['type']
            params = {k: v for k, v in config.items() if k != 'type'}
            result_df = _add_feature(result_df, feature_type, params, output_name=feature_key)
          # Case 2: Feature type with a list of configurations
        elif isinstance(config, list) and feature_key in list_feature_mappings:
            feature_type = list_feature_mappings[feature_key]
            for item_config in config:
                output_name = item_config.get('name')
                if not output_name:
                    logging.warning(f"Missing 'name' in a {feature_type} configuration, skipping.")
                    continue
                params = {k: v for k, v in item_config.items() if k != 'name'}
                result_df = _add_feature(result_df, feature_type, params, output_name)
        
        # Handle unknown list configurations
        elif isinstance(config, list):
            logging.warning(f"Unrecognized list configuration key '{feature_key}'. Valid list keys are: {', '.join(list_feature_mappings.keys())}.")
        
        # Case 3: Legacy format - single feature configuration
        else:
            result_df = _add_feature(result_df, feature_key, config)
    
    return result_df

def _add_feature(df: pd.DataFrame, feature_type: str, params: dict, output_name: str = None) -> pd.DataFrame:
    """
    Helper function to add a specific feature to the DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        feature_type (str): Type of feature to add ('sma', 'price_change_pct_1d', etc.).
        params (dict): Parameters for the feature calculation.
        output_name (str, optional): Custom name for the output column.
            If not provided, the default naming from the underlying function is used.
    
    Returns:
        pd.DataFrame: DataFrame with the new feature added.
    """
    result = None
    
    if feature_type == "sma":
        result = add_sma(df, **params)
    elif feature_type == "price_change_pct_1d":
        result = add_price_change_pct_1d(df, **params)
    elif feature_type == "volatility_nday":
        result = add_volatility_nday(df, **params)
    else:
        logging.warning(f"Feature type '{feature_type}' is not recognized and will be ignored.")
        return df
    
    # Rename the result if an output_name was provided
    if output_name and result is not None:
        result.name = output_name
    
    # Check if the column name already exists in the DataFrame to avoid conflicts
    if result is not None:
        column_name = result.name
        if column_name in df.columns:
            logging.warning(f"Column '{column_name}' already exists in DataFrame. Renaming to avoid collision.")
            # Append a suffix until a unique name is found
            suffix = 1
            while f"{column_name}_{suffix}" in df.columns:
                suffix += 1
            result.name = f"{column_name}_{suffix}"
            logging.info(f"Renamed column to '{result.name}'")
        
        # Join the result to the DataFrame
        df = df.join(result)
    
    return df
