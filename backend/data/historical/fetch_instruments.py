import pandas as pd
from backend.data.utils.kite import get_kite_client
from backend.db.connection import get_pg_connection
from datetime import datetime
import psycopg2

def fetch_instruments():
    kite = get_kite_client()
    instruments = kite.instruments()
    print(f"📦 Fetched instruments: {len(instruments)}")
    return pd.DataFrame(instruments)

def insert_instruments_to_db(df: pd.DataFrame):
    conn = get_pg_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO instruments (
        instrument_token, tradingsymbol, name, exchange, segment,
        instrument_type, expiry, strike, tick_size, lot_size, last_price
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (instrument_token) DO NOTHING
    """

    inserted = 0

    for _, row in df.iterrows():
        try:
            expiry = row.get("expiry")
            expiry = pd.to_datetime(expiry, errors="coerce").date() if pd.notna(expiry) and expiry != "" else None

            cur.execute(insert_query, (
                row["instrument_token"],
                row["tradingsymbol"],
                row["name"],
                row["exchange"],
                row["segment"],
                row["instrument_type"],
                expiry,
                row.get("strike"),
                row.get("tick_size"),
                row.get("lot_size"),
                row.get("last_price")
            ))

            inserted += 1

        except psycopg2.Error as e:
            print(f"❌ Skipping row due to DB error: {e}")
            conn.rollback()
            continue

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Instruments inserted: {inserted}")

if __name__ == "__main__":
    df = fetch_instruments()
    insert_instruments_to_db(df)
