# tests/test_strategies.py
import pytest

def test_strategies_module_can_be_imported():
    """
    Tests that the strategies module can be successfully imported.
    """
    import_failed = False
    try:
        import src.strategies
    except ImportError:
        import_failed = True
    assert not import_failed, "The module src.strategies could not be imported."

def test_base_strategy_class_exists():
    """
    Tests that a BaseStrategy class is available in the strategies module.
    """
    try:
        from src.strategies import BaseStrategy
        assert BaseStrategy is not None
    except ImportError:
        pytest.fail("Could not import BaseStrategy from src.strategies.")
