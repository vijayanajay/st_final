# Config Parser (`src/config_parser.py`)

This module provides utilities for loading and parsing configuration files.

## Functions

### `load_config(file_path: str) -> dict`

Loads a YAML configuration file from the given `file_path`.

**Arguments:**
- `file_path` (str): The path to the YAML configuration file.

**Returns:**
- `dict`: A dictionary representing the parsed YAML content.

**Raises:**
- `FileNotFoundError`: If the specified file does not exist.
- `yaml.YAMLError`: If the file content is not valid YAML.

## Usage Example

```python
from src.config_parser import load_config
import yaml # Added import for yaml.YAMLError

try:
    config = load_config("path/to/your/config.yaml")
    print("Setting1:", config.get("setting1"))
except FileNotFoundError:
    print("Error: Configuration file not found.")
except yaml.YAMLError: # Corrected to reference yaml.YAMLError
    print("Error: Invalid YAML format in configuration file.")
```
