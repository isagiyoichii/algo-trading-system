# backend/data/utils/export_to_csv.py

import os
import pandas as pd
import psycopg2
from backend.db.connection import get_db_connection

EXPORT_DIR = "exports/minute"

def export_to_csv(instrument_token: int, instrument_name: str):
    conn = get_db_connection()
    query = """
        SELECT timestamp, open, high, low, close, volume
        FROM ohlcv
        WHERE instrument_token = %s
        ORDER BY timestamp
    """
    df = pd.read_sql(query, conn, params=(instrument_token,))
    conn.close()

    if df.empty:
        print(f"[{instrument_name}] No data found.")
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)
    filename = f"{instrument_name.replace(' ', '_')}_minute.csv"
    path = os.path.join(EXPORT_DIR, filename)

    df.to_csv(path, index=False)
    print(f"[{instrument_name}] ✅ Exported to {path}")
