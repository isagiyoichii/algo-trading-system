import os
import time
import random
import datetime
from kiteconnect import KiteConnect, KiteException
from dotenv import load_dotenv
from backend.db.connection import get_pg_connection
from backend.data.utils.instrument_list import INDEX_INSTRUMENTS

# ——— CONFIG ———
INTERVAL = "minute"
MAX_DAYS_PER_REQUEST = 7
RETRY_MAX = 5
SLEEP_BETWEEN_CALLS = 1.0
START_DATE = datetime.datetime(2010, 1, 1)
END_DATE = datetime.datetime.now()

# ——— INIT ENV ———
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# ——— FETCH FUNCTION ———
def fetch_ohlcv(token: int, symbol: str):
    conn = get_pg_connection()
    cur = conn.cursor()

    print(f"\n📊 {symbol}: Fetching 1-min data...")

    start_date = START_DATE
    end_date = END_DATE
    batch = 1

    while start_date < end_date:
        to_date = min(start_date + datetime.timedelta(days=MAX_DAYS_PER_REQUEST), end_date)

        print(f"📦 {symbol} - Batch {batch}: {start_date.date()} ➝ {to_date.date()}")

        retry = 0
        while retry <= RETRY_MAX:
            try:
                candles = kite.historical_data(token, start_date, to_date, INTERVAL)
                if candles:
                    insert_query = """
                        INSERT INTO ohlcv (instrument_token, timestamp, open, high, low, close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """
                    cur.executemany(insert_query, [
                        (token, c["date"], c["open"], c["high"], c["low"], c["close"], c["volume"]) for c in candles
                    ])
                    conn.commit()
                    print(f"✅ {symbol} - Inserted {len(candles)} rows.")
                else:
                    print(f"⚠️ {symbol} - No data returned for this batch.")
                time.sleep(SLEEP_BETWEEN_CALLS + random.uniform(0, 0.5))
                break  # success
            except KiteException as e:
                if e.code == 429 or "Too many requests" in str(e):
                    retry += 1
                    wait = min(60, 2 ** retry) + random.uniform(0.5, 1.5)
                    print(f"⏳ {symbol} - Rate limited. Retry {retry}/{RETRY_MAX} after {wait:.1f}s...")
                    time.sleep(wait)
                else:
                    print(f"❌ {symbol}: Kite error: {e}")
                    return
            except Exception as e:
                print(f"❌ {symbol}: Unexpected error: {e}")
                return

        start_date = to_date + datetime.timedelta(seconds=1)
        batch += 1

    cur.close()
    conn.close()
    print(f"🏁 {symbol}: Completed fetching.\n")
    return {"symbol": symbol, "start": START_DATE.date(), "end": END_DATE.date()}

# ——— MAIN ———
if __name__ == "__main__":
    print("🔌 Connection established to Kite and Database.")
    summary = []
    for item in INDEX_INSTRUMENTS:
        token = item["token"]
        symbol = item["symbol"]
        result = fetch_ohlcv(token, symbol)
        if result:
            summary.append(result)

    print("\n📋 Summary Report:")
    for r in summary:
        print(f"✔️ {r['symbol']}: {r['start']} ➝ {r['end']}")
