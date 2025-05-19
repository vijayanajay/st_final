# tests/test_strategies.py
import pytest
import pandas as pd
from pandas.testing import assert_series_equal

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

def test_generate_sma_crossover_signals_basic():
    """
    Tests basic SMA crossover signal generation for BUY, SELL, and HOLD scenarios.
    """
    data = {
        'close': [10, 12, 13, 15, 14, 13, 12, 11, 13, 15],
        'SMA_short': [10, 11, 12, 13.5, 14, 13.5, 13, 12, 12.5, 14], # Example values
        'SMA_long':  [10, 10.5, 11, 11.5, 12.5, 13, 13.5, 13, 12.5, 12.5]  # Example values
    }
    df = pd.DataFrame(data)

    # Expected signals:
    # 0: Initial state, no signal (or HOLD if we define it that way)
    # 1: SMA_short (11) > SMA_long (10.5) - no crossover yet from previous, HOLD
    # 2: SMA_short (12) > SMA_long (11) - no crossover yet, HOLD
    # 3: SMA_short (13.5) > SMA_long (11.5) - BUY (short crossed above long: 12 > 11 prev, now 13.5 > 11.5, but the actual crossover happened when short became > long)
    #    Let's define crossover:
    #    SMA_short.shift(1) <= SMA_long.shift(1) AND SMA_short > SMA_long  => BUY (1)
    #    SMA_short.shift(1) >= SMA_long.shift(1) AND SMA_short < SMA_long  => SELL (-1)
    #    Else HOLD (0)

    # Recalculating expected based on precise crossover logic:
    # Period 0: SMA_short=10, SMA_long=10. Prev_short=NaN, Prev_long=NaN. Signal: 0 (HOLD)
    # Period 1: SMA_short=11, SMA_long=10.5. Prev_short=10, Prev_long=10. (10 <= 10) and (11 > 10.5) => BUY (1)
    # Period 2: SMA_short=12, SMA_long=11. Prev_short=11, Prev_long=10.5. (11 > 10.5) and (12 > 11) => HOLD (0)
    # Period 3: SMA_short=13.5, SMA_long=11.5. Prev_short=12, Prev_long=11. (12 > 11) and (13.5 > 11.5) => HOLD (0)
    # Period 4: SMA_short=14, SMA_long=12.5. Prev_short=13.5, Prev_long=11.5. (13.5 > 11.5) and (14 > 12.5) => HOLD (0)
    # Period 5: SMA_short=13.5, SMA_long=13. Prev_short=14, Prev_long=12.5. (14 > 12.5) and (13.5 > 13) => HOLD (0)
    # Period 6: SMA_short=13, SMA_long=13.5. Prev_short=13.5, Prev_long=13. (13.5 > 13) and (13 < 13.5) => SELL (-1)
    # Period 7: SMA_short=12, SMA_long=13. Prev_short=13, Prev_long=13.5. (13 < 13.5) and (12 < 13) => HOLD (0)
    # Period 8: SMA_short=12.5, SMA_long=12.5. Prev_short=12, Prev_long=13. (12 < 13) and (12.5 == 12.5) => HOLD (0)
    # Period 9: SMA_short=14, SMA_long=12.5. Prev_short=12.5, Prev_long=12.5. (12.5 == 12.5) and (14 > 12.5) => BUY (1)

    expected_signals = pd.Series([0, 1, 0, 0, 0, 0, -1, 0, 0, 1], name="signal")

    from src.strategies import generate_sma_crossover_signals
    actual_signals = generate_sma_crossover_signals(df.copy(), short_window=5, long_window=10) # windows are illustrative

    assert_series_equal(actual_signals, expected_signals, check_dtype=False)
