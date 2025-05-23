# Module: src/config_parser.py

## Overview

The `config_parser.py` module is responsible for loading and validating YAML configuration files for trading strategies. It ensures that all required fields are present and that the configuration is properly formatted.

## Key Function

### `load_config(filepath: str, validate_schema: bool = True) -> dict`

**Parameters:**
- `filepath` (str): Path to the YAML config file.
- `validate_schema` (bool, optional): Whether to validate the config schema. Defaults to True. When False, only loads and returns the config without validation.

**Returns:**
- `dict`: Parsed configuration.

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `ValueError`: If YAML is invalid or required fields are missing.

**Logging:**
- Logs events at the `ERROR` level when file is not found, YAML parsing fails, or required fields are missing.
- Logs at the `INFO` level when config is loaded successfully.
- All log messages use standard error types and follow consistent patterns for testability and observability.

## Function Details: load_config

```python
def load_config(filepath: str, validate_schema: bool = True) -> dict
```
- Loads and validates YAML configuration files for trading strategies.
- Supports two configuration formats:
- When `validate_schema` is True (default), performs strict schema validation and ensures all required fields are present.
- When `validate_schema` is False, only loads the YAML file and returns its contents without validation, useful for testing or when validation is handled elsewhere.

### Legacy Format
```yaml
strategy: sma_cross
fast_window: 10
slow_window: 50
```

### New Format
```yaml
strategy_name: sma_crossover
parameters:
  short_window: 20
  long_window: 50
```

## Example Usage

```python
from src import config_parser

try:
    config = config_parser.load_config('configs/strategies/sma_cross.yaml')
    print(config)
    
    # Load without schema validation
    config_unvalidated = config_parser.load_config('configs/strategies/sma_cross.yaml', validate_schema=False)
    print(config_unvalidated)
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
```

## Required Configuration Fields

The module validates that all required fields are present in the configuration:

### Legacy Format Required Fields
- `strategy`: The name of the trading strategy to use.
- `fast_window`: The window size for the fast moving average.
- `slow_window`: The window size for the slow moving average.

### New Format Required Fields
- `strategy_name`: The name of the trading strategy to use.
- `parameters`: Dictionary containing strategy parameters.
  - `short_window`: The window size for the short moving average.
  - `long_window`: The window size for the long moving average.

## Testing

The module is tested in `tests/test_config_parser.py`, which includes tests for:
- Loading valid configurations in both legacy and new formats
- Handling missing files
- Handling invalid YAML
- Handling missing required fields

The tests verify both the correct behavior of the function and the appropriate logging of events.

## Notes on Log Capture in Tests

Tests for this module use pytest's `caplog` fixture to verify log messages. When accessing log messages in tests:

1. Individual log records should be accessed through `caplog.records` rather than `caplog.text`
2. The expected substrings should be checked against each record's `message` attribute

```python
# Example test that verifies a log message
def test_example(caplog):
    with pytest.raises(SomeException):
        function_that_should_log()
    assert any('expected phrase' in record.message.lower() for record in caplog.records)
```
