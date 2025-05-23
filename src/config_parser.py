import yaml
import logging
import os

def load_config(filepath: str, validate_schema: bool = True) -> dict:
    """
    Loads and validates YAML configuration files for trading strategies.
    Supports both legacy and new format configurations.
    If validate_schema is True, performs strict schema validation; otherwise, only loads and returns the config.
    
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
        filepath (str): Path to the YAML config file.
        validate_schema (bool): Whether to validate the config schema.
        
    Returns:
        dict: Parsed configuration with required fields.
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If YAML is invalid or required fields are missing.
    """
    logger = logging.getLogger(__name__)
    if not os.path.exists(filepath):
        logger.error(f"Config file not found (not found): {filepath}")
        raise FileNotFoundError(f"Config file not found: {filepath}")
    try:
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error (yaml): {filepath}: {e}")
        raise ValueError(f"YAML parsing error in {filepath}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading YAML (yaml) from {filepath}: {e}")
        raise
    
    if not isinstance(config, dict):
        logger.error(f"YAML structure error (yaml) in {filepath}: Top-level object is not a dictionary.")
        raise ValueError(f"YAML structure error in {filepath}: Top-level object is not a dictionary.")
    
    if not validate_schema:
        logger.info(f"Loaded config from {filepath} (schema validation skipped).")
        return config

    # Check if it's a legacy format (has 'strategy' instead of 'strategy_name')
    if 'strategy' in config and 'strategy_name' not in config:
        # Legacy format validation
        required_legacy_fields = {'strategy', 'fast_window', 'slow_window'}
        missing = required_legacy_fields - set(config.keys())
        if missing:
            logger.error(f"YAML validation error (missing required) in {filepath}: Missing required fields: {missing}")
            raise ValueError(f"YAML validation error in {filepath}: Missing required fields: {missing}")
        logger.info(f"Loaded config (legacy format) from {filepath} successfully.")
    else:
        # New format validation
        if 'strategy_name' not in config or 'parameters' not in config:
            logger.error(f"YAML validation error (missing required) in {filepath}: Missing 'strategy_name' or 'parameters'")
            raise ValueError(f"YAML validation error in {filepath}: Missing 'strategy_name' or 'parameters'")
        
        required_param_fields = {'short_window', 'long_window'}
        missing = required_param_fields - set(config['parameters'].keys())
        if missing:
            logger.error(f"YAML validation error (missing required) in {filepath}: Missing required parameter fields: {missing}")
            raise ValueError(f"YAML validation error in {filepath}: Missing required parameter fields: {missing}")
        logger.info(f"Loaded config (new format) from {filepath} successfully.")
    
    return config
