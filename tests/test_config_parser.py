import pytest
import os
import tempfile
import yaml
from src import config_parser

@pytest.fixture
def valid_yaml_file():
    data = {'strategy': 'sma_cross', 'fast_window': 10, 'slow_window': 50}
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

def test_load_valid_config(valid_yaml_file):
    config = config_parser.load_config(valid_yaml_file)
    assert config['strategy'] == 'sma_cross'
    assert config['fast_window'] == 10
    assert config['slow_window'] == 50

def test_load_missing_file(missing_file, caplog):
    with pytest.raises(FileNotFoundError):
        config_parser.load_config(missing_file)
    # Access individual log records instead of using caplog.text
    assert any('not found' in record.message.lower() for record in caplog.records)

def test_load_invalid_yaml(invalid_yaml_file, caplog):
    with pytest.raises(ValueError):
        config_parser.load_config(invalid_yaml_file)
    # Access individual log records instead of using caplog.text
    assert any('yaml' in record.message.lower() for record in caplog.records)

def test_missing_required_fields(valid_yaml_file, caplog):
    # Remove a required field
    with open(valid_yaml_file, 'w') as f:
        yaml.dump({'strategy': 'sma_cross', 'fast_window': 10}, f)
    with pytest.raises(ValueError):
        config_parser.load_config(valid_yaml_file)
    # Access individual log records instead of using caplog.text
    assert any('missing required' in record.message.lower() for record in caplog.records)

def test_load_sample_sma_cross_config():
    path = os.path.join(os.path.dirname(__file__), '../configs/strategies/sma_cross.yaml')
    path = os.path.abspath(path)
    config = config_parser.load_config(path)
    # The new config uses 'strategy_name' and 'parameters' keys
    assert config['strategy_name'] == 'sma_crossover'
    assert 'parameters' in config
    assert config['parameters']['short_window'] == 20
    assert config['parameters']['long_window'] == 50
