from pydantic import BaseModel

class Trade(BaseModel):
    symbol: str
    qty: int
    price: float
