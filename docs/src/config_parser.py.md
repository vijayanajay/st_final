<!-- filepath: d:\Code\st_final\docs\src\config_parser.py.md -->
# Module: src/config_parser.py

## Overview

The `config_parser.py` module is responsible for loading and validating YAML configuration files for trading strategies. It ensures that all required fields are present and that the configuration is properly formatted.

## Key Function

### `load_config(path: str) -> dict`

**Parameters:**
- `path` (str): Path to the YAML config file.

**Returns:**
- `dict`: Parsed configuration.

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `ValueError`: If YAML is invalid or required fields are missing.

**Logging:**
- Logs events at the `ERROR` level when file is not found, YAML parsing fails, or required fields are missing.
- Logs at the `INFO` level when config is loaded successfully.
- All log messages use standard error types and follow consistent patterns for testability and observability.

## Example Usage

```python
from src import config_parser

try:
    config = config_parser.load_config('configs/strategies/sma_cross.yaml')
    print(config)
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
```

## Required Configuration Fields

The module validates that all of the following fields are present in the configuration:
- `strategy`: The name of the trading strategy to use.
- `fast_window`: The window size for the fast moving average.
- `slow_window`: The window size for the slow moving average.

## Testing

The module is tested in `tests/test_config_parser.py`, which includes tests for:
- Loading valid configurations
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
