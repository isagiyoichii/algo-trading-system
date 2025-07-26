from dataclasses import dataclass
from typing import Dict

@dataclass
class Position:
    quantity: int = 0
    avg_price: float = 0.0

def _update_avg_price(old_qty: int, old_price: float, qty: int, price: float) -> float:
    new_qty = old_qty + qty
    if new_qty == 0:
        return 0.0
    return ((old_price * old_qty) + qty * price) / new_qty

class Portfolio:
    """Track cash and positions and compute portfolio value."""

    def __init__(self, cash: float = 0.0):
        self.cash = cash
        self.positions: Dict[str, Position] = {}
        self.trades = []

    def execute_trade(self, symbol: str, qty: int, price: float):
        self.cash -= qty * price
        pos = self.positions.get(symbol, Position())
        pos.avg_price = _update_avg_price(pos.quantity, pos.avg_price, qty, price)
        pos.quantity += qty
        self.positions[symbol] = pos
        self.trades.append({"symbol": symbol, "qty": qty, "price": price})

    def market_value(self, prices: Dict[str, float]) -> float:
        value = self.cash
        for sym, pos in self.positions.items():
            value += pos.quantity * prices.get(sym, pos.avg_price)
        return value
