import pytest
import os
import yaml
import logging
from src import config_parser

import tempfile

import sys

import types

import importlib

def make_legacy_config():
    return {'strategy': 'sma_cross', 'fast_window': 10, 'slow_window': 50}

def make_new_config():
    return {'strategy_name': 'sma_crossover', 'parameters': {'short_window': 20, 'long_window': 50}}

@pytest.fixture
def valid_legacy_yaml_file():
    data = make_legacy_config()
    with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as f:
        yaml.dump(data, f)
        yield f.name
    os.remove(f.name)

@pytest.fixture
def valid_new_yaml_file():
    data = make_new_config()
    with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as f:
        yaml.dump(data, f)
        yield f.name
    os.remove(f.name)

@pytest.fixture
def invalid_yaml_file():
    with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as f:
        f.write('strategy: [unclosed_list\n')
        yield f.name
    os.remove(f.name)

@pytest.fixture
def missing_file():
    return 'nonexistent_file.yaml'

def test_load_valid_legacy_config(valid_legacy_yaml_file, caplog):
    with caplog.at_level(logging.INFO):
        config = config_parser.load_config(valid_legacy_yaml_file)
    assert config['strategy'] == 'sma_cross'
    assert config['fast_window'] == 10
    assert config['slow_window'] == 50
    assert any('loaded config (legacy format)' in record.message.lower() for record in caplog.records)

def test_load_valid_new_config(valid_new_yaml_file, caplog):
    with caplog.at_level(logging.INFO):
        config = config_parser.load_config(valid_new_yaml_file)
    assert config['strategy_name'] == 'sma_crossover'
    assert 'parameters' in config
    assert config['parameters']['short_window'] == 20
    assert config['parameters']['long_window'] == 50
    assert any('loaded config (new format)' in record.message.lower() for record in caplog.records)

def test_load_missing_file(missing_file, caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(FileNotFoundError):
            config_parser.load_config(missing_file)
    assert any('not found' in record.message.lower() for record in caplog.records)

def test_load_invalid_yaml(invalid_yaml_file, caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            config_parser.load_config(invalid_yaml_file)
    assert any('yaml' in record.message.lower() for record in caplog.records)

def test_missing_required_fields(valid_legacy_yaml_file, caplog):
    # Remove a required field from legacy config
    with open(valid_legacy_yaml_file, 'w') as f:
        yaml.dump({'strategy': 'sma_cross', 'fast_window': 10}, f)
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            config_parser.load_config(valid_legacy_yaml_file)
    assert any('missing required' in record.message.lower() for record in caplog.records)

def test_missing_required_fields_new(valid_new_yaml_file, caplog):
    # Remove a required parameter from new config
    with open(valid_new_yaml_file, 'w') as f:
        yaml.dump({'strategy_name': 'sma_crossover', 'parameters': {'short_window': 20}}, f)
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            config_parser.load_config(valid_new_yaml_file)
    assert any('missing required' in record.message.lower() for record in caplog.records)

def test_load_sample_sma_cross_config():
    path = os.path.join(os.path.dirname(__file__), '../configs/strategies/sma_cross.yaml')
    path = os.path.abspath(path)
    config = config_parser.load_config(path)
    assert config['strategy_name'] == 'sma_crossover'
    assert 'parameters' in config
    assert config['parameters']['short_window'] == 20
    assert config['parameters']['long_window'] == 50

def test_load_config_signature_and_behavior():
    import inspect
    from src import config_parser
    sig = inspect.signature(config_parser.load_config)
    assert list(sig.parameters.keys()) == ["filepath", "validate_schema"]
    # Behavioral tests for error handling and legacy/new format support are covered in other dedicated test functions.
