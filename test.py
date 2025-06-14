from backend.data.historical.insert_ohlcv import insert_ohlcv
import pandas as pd

# Mock data
df = pd.DataFrame([{
    'timestamp': '2024-01-01 09:15:00',
    'open': 22000,
    'high': 22100,
    'low': 21900,
    'close': 22050,
    'volume': 123456
}])

insert_ohlcv(df, instrument_token=256265)  # NIFTY 50
