import pandas as pd

class Order:
    def __init__(self, timestamp, price, quantity, direction):
        self.timestamp = timestamp
        self.price = price
        self.quantity = quantity
        self.direction = direction  # 'BUY' or 'SELL'

class BacktestEngine:
    """Simple OHLCV backtester with market order simulation."""

    def __init__(self, cash=100000):
        self.initial_cash = cash
        self.cash = cash
        self.position = 0
        self.orders = []
        self.equity_curve = []

    def buy(self, timestamp, price, qty):
        cost = price * qty
        if self.cash >= cost:
            self.cash -= cost
            self.position += qty
            self.orders.append(Order(timestamp, price, qty, 'BUY'))

    def sell(self, timestamp, price, qty):
        if self.position >= qty:
            self.cash += price * qty
            self.position -= qty
            self.orders.append(Order(timestamp, price, qty, 'SELL'))

    def run(self, data: pd.DataFrame, strategy):
        """Run strategy on OHLCV DataFrame.
        Strategy must implement generate_signals(data) returning Series with
        'BUY', 'SELL', or None for each row.
        """
        signals = strategy.generate_signals(data)
        for idx, row in data.iterrows():
            signal = signals.loc[idx]
            if signal == 'BUY':
                self.buy(row['timestamp'], row['close'], 1)
            elif signal == 'SELL':
                self.sell(row['timestamp'], row['close'], 1)
            equity = self.cash + self.position * row['close']
            self.equity_curve.append({'timestamp': row['timestamp'], 'equity': equity})
        return pd.DataFrame(self.equity_curve)
