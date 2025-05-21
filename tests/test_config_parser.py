import pytest
import yaml # For yaml.YAMLError
from src.config_parser import load_config
import os

# Define fixture paths (adjust if worker has different CWD)
VALID_CONFIG_PATH = "tests/fixtures/valid_config.yaml"
INVALID_CONFIG_PATH = "tests/fixtures/invalid_config.yaml"
NON_EXISTENT_PATH = "tests/fixtures/non_existent_config.yaml"

def test_load_valid_config():
    """Tests loading a valid YAML file."""
    expected_dict = {
        "setting1": "value1",
        "setting2": 123,
        "nested": {"sub_setting": True},
    }
    assert load_config(VALID_CONFIG_PATH) == expected_dict

def test_load_non_existent_file():
    """Tests loading a non-existent YAML file."""
    with pytest.raises(FileNotFoundError):
        load_config(NON_EXISTENT_PATH)

def test_load_invalid_yaml():
    """Tests loading a file with invalid YAML syntax."""
    with pytest.raises(yaml.YAMLError):
        load_config(INVALID_CONFIG_PATH)

# Optional: A small test to ensure fixture files were created, can be removed by worker if redundant
def test_fixture_files_exist():
    assert os.path.exists(VALID_CONFIG_PATH)
    assert os.path.exists(INVALID_CONFIG_PATH)
