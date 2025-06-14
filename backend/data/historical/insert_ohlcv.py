# backend/data/historical/insert_ohlcv.py

import pandas as pd
import psycopg2
from backend.db.connection import get_db_connection

def insert_ohlcv(df: pd.DataFrame, instrument_token: int):
    if df.empty:
        print(f"[{instrument_token}] ⚠️ Skipped — empty DataFrame")
        return

    try:
        # Standardize timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.floor('min')
        df['instrument_token'] = instrument_token

        # Ensure required columns exist
        required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            print(f"[{instrument_token}] ❌ Missing columns in DataFrame. Found: {list(df.columns)}")
            return

        # Arrange columns in exact order
        records = df[['timestamp', 'instrument_token', 'open', 'high', 'low', 'close', 'volume']].values.tolist()

        insert_query = """
            INSERT INTO ohlcv (timestamp, instrument_token, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp, instrument_token) DO NOTHING;
        """

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany(insert_query, records)
        conn.commit()

        print(f"[{instrument_token}] ✅ Inserted: {len(records)} rows")

    except Exception as e:
        print(f"[{instrument_token}] ❌ Error during insertion: {e}")
        if 'records' in locals() and records:
            print(f"[{instrument_token}] ⚠️ First record attempted: {records[0]}")
        else:
            print(f"[{instrument_token}] ⚠️ No records attempted.")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
