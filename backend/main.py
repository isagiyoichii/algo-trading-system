from typing import List
import pandas as pd
from fastapi import FastAPI
from backend.backtesting.report import compute_drawdown

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Algo trading backend is running 🚀"}

@app.post("/analytics/drawdown")
def analytics_drawdown(equity: List[float]):
    series = pd.Series(equity)
    dd = compute_drawdown(series)
    return {"drawdown": dd.tolist()}
