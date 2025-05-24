# tests/test_config_parser.py

## Purpose
Unit tests for `src/config_parser.py`. Ensures correct loading, validation, and error handling for YAML strategy configuration files.

## Key Test Functions
- `test_load_valid_config`: Verifies correct parsing of valid config files.
- `test_missing_file`: Ensures FileNotFoundError is raised for missing files.
- `test_invalid_yaml`: Checks ValueError for invalid YAML.
- `test_missing_required_fields`: Ensures ValueError for missing required fields.
- Logging tests: Verifies error and info logs using pytest's `caplog`.

## Coverage
- Valid/invalid config loading
- Schema validation toggle
- Error handling and logging

## Notes
- Uses fixtures for sample configs.
- Extensible for new config schema changes.
