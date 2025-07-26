import pandas as pd

class BaseStrategy:
    """Base class for strategies used with BacktestEngine."""

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Return Series indexed same as data with 'BUY'/'SELL'/None."""
        raise NotImplementedError

class MovingAverageCrossStrategy(BaseStrategy):
    def __init__(self, fast: int = 5, slow: int = 20):
        self.fast = fast
        self.slow = slow

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        fast_ma = data['close'].rolling(self.fast).mean()
        slow_ma = data['close'].rolling(self.slow).mean()
        signals = pd.Series(index=data.index, dtype=object)
        prev = None
        for i in range(len(data)):
            if pd.isna(fast_ma[i]) or pd.isna(slow_ma[i]):
                signals.iloc[i] = None
                continue
            if fast_ma[i] > slow_ma[i] and prev != 'LONG':
                signals.iloc[i] = 'BUY'
                prev = 'LONG'
            elif fast_ma[i] < slow_ma[i] and prev != 'SHORT':
                signals.iloc[i] = 'SELL'
                prev = 'SHORT'
            else:
                signals.iloc[i] = None
        return signals
