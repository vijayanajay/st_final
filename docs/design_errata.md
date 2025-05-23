# Design Errata and Implementation Notes

This document contains important notes about discrepancies between the original design documentation (`design.md`) and the actual implementation in the codebase. It highlights where implementation has evolved beyond the initial design and provides accurate information about the current state of the system.

## DOC-002: `feature_generator.py` - `generate_features` Implementation

**Category:** Documentation Mismatch (Design vs. Implementation)  
**Affected Documents:** docs/design.md (Section 4.4) vs. src/feature_generator.py, docs/src/feature_generator.py.md, docs/codebase_overview.md

### Discrepancy Description

The original design document (`design.md`, section 4.4) describes the `generate_features` function's `feature_config` parameter in a way that implies it's primarily derived from strategy parameters. The actual implementation has evolved to provide a more flexible and powerful feature configuration structure.

### Current Implementation (Accurate Documentation)

For the accurate and current specification of the `feature_config` parameter for `generate_features`, please refer to:
- [docs/src/feature_generator.py.md](src/feature_generator.py.md)
- [docs/codebase_overview.md](codebase_overview.md) (section on feature_generator.py)

The `generate_features` function supports three different ways to structure the `feature_config` parameter:

#### 1. Named Feature Instances with a 'type' Field
```python
{
    "SMA_short": {"type": "sma", "column": "close", "window": 20},
    "SMA_long": {"type": "sma", "column": "close", "window": 50},
    "Custom_Volatility": {"type": "volatility_nday", "column": "close", "window": 30}
}
```
In this format:
- The dictionary keys (e.g., "SMA_short") are used as the names for the resulting feature columns
- Each value is a dictionary that must include a "type" field specifying the feature type
- Other fields provide parameters for the specific feature calculation

#### 2. Predefined List Keys for Multiple Configurations of the Same Feature Type
```python
{
    "smas": [
        {"name": "SMA_short", "column": "close", "window": 20},
        {"name": "SMA_long", "column": "close", "window": 50}
    ],
    "volatility_metrics": [
        {"name": "volatility_20", "column": "close", "window": 20}
    ]
}
```
In this format:
- Predefined list keys ("smas", "price_changes", "volatility_metrics") group multiple configurations of the same feature type
- Each item in the list must include a "name" field to specify the output column name
- Valid list keys are: `"smas"`, `"price_changes"`, `"volatility_metrics"`

#### 3. Legacy Format (for Backward Compatibility)
```python
{
    "sma": {"column": "close", "window": 20},
    "price_change_pct_1d": {"column": "close"},
    "volatility_nday": {"column": "close", "window": 20}
}
```
In this format:
- The dictionary keys specify the feature type directly
- Each value is a dictionary providing parameters for that feature
- Output column names are determined by the underlying feature functions

### Additional Implementation Details

The current implementation includes these important behaviors not mentioned in the original design:

1. **Column Name Conflict Resolution**: If a generated feature's column name already exists in the DataFrame, the function will automatically rename the new column by appending a numerical suffix (e.g., `sma_3_1`, `sma_3_2`) to avoid overwriting existing data.

2. **Comprehensive Logging**: The implementation includes structured logging for all error conditions and critical operations, with configuration centralized in `configs/logging_config.py`.

3. **Advanced Error Handling**: Robust input validation and error handling ensure graceful failure with informative error messages.

For implementation details, usage examples, and API reference, please consult the updated documentation in `docs/src/feature_generator.py.md` and the example usage in `docs/codebase_overview.md`.
