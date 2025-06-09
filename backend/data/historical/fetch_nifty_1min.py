import os
import datetime
import time
import psycopg2
import logging
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from backend.db.connection import get_pg_connection

# ────────────────────────────────
# 🔧 CONFIGURATION
# ────────────────────────────────

INTERVAL = "minute"
MAX_DAYS_PER_REQUEST = 60
SLEEP_BETWEEN_CALLS = 0.5  # seconds

# ────────────────────────────────
# 🔧 ENV + LOGGER
# ────────────────────────────────

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

logging.basicConfig(
    filename="logs/fetch_nifty_1min.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ────────────────────────────────
# 🔗 INIT KITE
# ────────────────────────────────

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# ────────────────────────────────
# 🧠 Get instrument_token for NIFTY 50 Index (Spot)
# ────────────────────────────────

def get_nifty50_token():
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT instrument_token FROM instruments
            WHERE tradingsymbol = 'NIFTY 50' AND exchange = 'NSE'
            LIMIT 1
        """)
        result = cur.fetchone()
        cur.close()
        conn.close()
        if not result:
            raise ValueError("❌ NIFTY 50 not found in instruments table.")
        return result[0]
    except Exception as e:
        print("❌ Error fetching NIFTY token:", e)
        raise

# ────────────────────────────────
# ⛓️ Fetch and insert OHLCV data
# ────────────────────────────────

def fetch_full_nifty_ohlcv(token: int):
    conn = get_pg_connection()
    cur = conn.cursor()

    end_date = datetime.datetime.now()
    total_inserted = 0
    batch_count = 0

    # Try back to 2014-01-01 or earlier
    start_date = datetime.datetime(2017, 1, 1)

    print(f"🔁 Fetching full 1-min OHLCV for token: {token}")
    logging.info(f"Start fetching for token {token} from {start_date.date()} to {end_date.date()}")

    while start_date < end_date:
        from_date = start_date
        to_date = min(start_date + datetime.timedelta(days=MAX_DAYS_PER_REQUEST), end_date)

        try:
            print(f"📅 {from_date.date()} → {to_date.date()}")
            candles = kite.historical_data(token, from_date, to_date, INTERVAL)

            if not candles:
                print("⛔ No more data returned. Ending loop.")
                break

            for candle in candles:
                cur.execute("""
                    INSERT INTO ohlcv (
                        instrument_token, timestamp, open, high, low, close, volume, interval
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    token,
                    candle["date"],
                    candle["open"],
                    candle["high"],
                    candle["low"],
                    candle["close"],
                    candle["volume"],
                    INTERVAL
                ))

            conn.commit()
            inserted = len(candles)
            total_inserted += inserted
            batch_count += 1
            print(f"✅ Batch {batch_count}: Inserted {inserted} rows")
            logging.info(f"Batch {batch_count}: Inserted {inserted} rows for {from_date.date()} → {to_date.date()}")

        except Exception as e:
            conn.rollback()
            print(f"❌ Error: {e}")
            logging.error(f"Error for {from_date.date()} → {to_date.date()}: {e}")

        start_date = to_date + datetime.timedelta(days=1)
        time.sleep(SLEEP_BETWEEN_CALLS)

    cur.close()
    conn.close()
    print(f"\n🎯 Completed. Total 1-min rows inserted: {total_inserted}")
    logging.info(f"Completed. Total rows inserted: {total_inserted}")

# ────────────────────────────────
# 🏁 MAIN
# ────────────────────────────────

if __name__ == "__main__":
    try:
        token = get_nifty50_token()
        fetch_full_nifty_ohlcv(token)
    except Exception as e:
        print("❌ Terminated due to error:", e)
        logging.error(f"Fatal error: {e}")
