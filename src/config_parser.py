import yaml
import logging
import os

def load_config(path: str) -> dict:
    """
    Loads and validates YAML configuration files for trading strategies.
    Supports both legacy and new format configurations.
    
    Legacy format:
    {
        'strategy': 'sma_cross',
        'fast_window': 10,
        'slow_window': 50
    }
    
    New format:
    {
        'strategy_name': 'sma_crossover',
        'parameters': {
            'short_window': 20, 
            'long_window': 50
        }
    }
    
    Args:
        path (str): Path to the YAML config file.
    Returns:
        dict: Parsed configuration with required fields.
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If YAML is invalid or required fields are missing.
    """
    logger = logging.getLogger(__name__)
    if not os.path.exists(path):
        logger.error(f"Config file not found (not found): {path}")
        raise FileNotFoundError(f"Config file not found: {path}")
    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error (yaml): {path}: {e}")
        raise ValueError(f"YAML parsing error in {path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading YAML (yaml) from {path}: {e}")
        raise
    
    if not isinstance(config, dict):
        logger.error(f"YAML structure error (yaml) in {path}: Top-level object is not a dictionary.")
        raise ValueError(f"YAML structure error in {path}: Top-level object is not a dictionary.")
    
    # Check if it's a legacy format (has 'strategy' instead of 'strategy_name')
    if 'strategy' in config and 'strategy_name' not in config:
        # Legacy format validation
        required_legacy_fields = {'strategy', 'fast_window', 'slow_window'}
        missing = required_legacy_fields - set(config.keys())
        if missing:
            logger.error(f"YAML validation error (missing required) in {path}: Missing required fields: {missing}")
            raise ValueError(f"YAML validation error in {path}: Missing required fields: {missing}")
        logger.info(f"Loaded config (legacy format) from {path} successfully.")
    else:
        # New format validation
        if 'strategy_name' not in config or 'parameters' not in config:
            logger.error(f"YAML validation error (missing required) in {path}: Missing 'strategy_name' or 'parameters'")
            raise ValueError(f"YAML validation error in {path}: Missing 'strategy_name' or 'parameters'")
        
        required_param_fields = {'short_window', 'long_window'}
        missing = required_param_fields - set(config['parameters'].keys())
        if missing:
            logger.error(f"YAML validation error (missing required) in {path}: Missing required parameter fields: {missing}")
            raise ValueError(f"YAML validation error in {path}: Missing required parameter fields: {missing}")
        logger.info(f"Loaded config (new format) from {path} successfully.")
    
    return config
