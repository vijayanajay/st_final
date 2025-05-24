# tests/test_integration.py.md

# Integration Test Module Documentation

## Overview
The `tests/test_integration.py` file contains integration tests for the Simple Stock Strategy Backtester (S3B). These tests verify that multiple modules work together correctly, including feature generation and strategy implementation integration.

## Test Structure

### `test_feature_generation_and_strategy_integration`
- **Purpose:** Integration test to verify that feature generation and SMA crossover strategy work together correctly with multiple SMA configurations.
- **Test Logic:**
  - Creates sample price data with a simple price series
  - Configures feature generation with short and long SMAs
  - Verifies both SMA columns are correctly generated
  - Uses `apply_strategy` with an SMA crossover configuration to generate signals
  - Verifies signals are correctly generated (values are -1, 0, or 1)
  - Performs basic sanity checks on the number of buy, sell, and hold signals
- **API Usage:** Uses the recommended primary `apply_strategy` API from `src.strategies`

### `test_legacy_feature_config_integration`
- **Purpose:** Integration test to verify backward compatibility with legacy feature configuration format.
- **Test Logic:**
  - Creates sample price data
  - Tests using the legacy feature config format (without explicit feature type)
  - Verifies that SMA column is present with legacy naming convention
  - Validates data integrity (preservation of row count, no NaN values in the close price)
- **API Usage:** Tests backward compatibility while still using modern patterns

### `test_multiple_feature_types_integration`
- **Purpose:** Integration test to verify that multiple feature types can be generated together.
- **Test Logic:**
  - Creates sample price data
  - Configures multiple feature types (SMA, price change percentage, volatility)
  - Verifies all feature columns are present
  - Checks data types of generated features
  - Tests applying a strategy to the generated features
- **API Usage:** Uses the recommended primary `apply_strategy` API from `src.strategies`

### `test_end_to_end_integration_with_results_file`
- **Purpose:** Comprehensive end-to-end integration test that generates a results file for manual inspection, replacing the standalone `integration_test.py` functionality.
- **Test Logic:**
  - Creates sample price data
  - Generates features using named feature config format
  - Applies a strategy using the primary API (`apply_strategy`)
  - Generates a detailed results file for manual inspection
  - Verifies all components work together correctly
  - Maintains the output format of the original standalone integration test
- **Notes:**
  - This test writes results to a temporary path using pytest's `tmp_path` fixture
  - For compatibility, it also creates a copy in the project root named `integration_test_results.txt` (which is gitignored)
  - This test replaces the functionality previously in the standalone `integration_test.py` script
- **API Usage:** Uses the recommended primary `apply_strategy` API from `src.strategies`

## File Output
- Generates `integration_test_results.txt` in the project root for manual inspection
- Contains DataFrame visualizations, signal analysis, and test completion information
- The file is included in `.gitignore` to prevent versioning of test output files

## Migration Note
This file was created as part of refactoring the original standalone `integration_test.py` script into proper pytest-compatible test functions. The original script utilized a legacy API function (`generate_sma_crossover_signals`), while these tests use the recommended primary API (`apply_strategy`) as per documented best practices.

## Key Testing Principles

### Integration Testing Focus
These tests focus on verifying the interaction between multiple components:
1. **End-to-End Verification**: Tests complete workflows from data preparation through feature generation to strategy application
2. **Cross-Module Integration**: Verifies that separate modules like `feature_generator.py` and `strategies.py` work together correctly
3. **API Consistency**: Ensures that the recommended APIs are used consistently across the codebase

### Pytest Integration
- All tests are properly integrated with pytest using the `@pytest.mark.integration` decorator
- This allows selective running of integration tests (e.g., `pytest -m integration`)
- Tests are discoverable through standard pytest mechanisms

### Output File Management  
- The output file generation uses pytest's `tmp_path` fixture for clean test isolation
- A copy is maintained in the project root for backward compatibility and manual inspection
- The output files are properly excluded from version control via `.gitignore`
