import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import os
import time
import datetime
import pandas as pd
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from backend.data.utils.instrument_list import INDEX_INSTRUMENTS
from backend.data.historical.insert_ohlcv import insert_ohlcv  # NEW IMPORT

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────

INTERVAL = "minute"
MAX_DAYS_PER_REQUEST = 60
RETRY_INCREMENT_DAYS = 7
SLEEP_BETWEEN_CALLS = 0.5
START_DATE = datetime.datetime(2010, 1, 1)
END_DATE = datetime.datetime.now()

# ─────────────────────────────────────────────────────────────
# ENV & API
# ─────────────────────────────────────────────────────────────

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# ─────────────────────────────────────────────────────────────
# FETCH FUNCTION
# ─────────────────────────────────────────────────────────────

def fetch_ohlcv(token: int, symbol: str) -> dict:
    print(f"\n📈 {symbol} ({token}) → Fetching 1-min OHLCV")

    start_date = START_DATE
    end_date = END_DATE
    total_inserted = 0
    batch_count = 0

    while start_date < end_date:
        from_date = start_date
        to_date = min(from_date + datetime.timedelta(days=MAX_DAYS_PER_REQUEST), end_date)

        try:
            candles = kite.historical_data(
                instrument_token=token,
                from_date=from_date,
                to_date=to_date,
                interval=INTERVAL,
                continuous=False
            )

            if not candles:
                print(f"⚠️  No data from {from_date.date()} → retrying from +1y...")
                start_date += datetime.timedelta(days=365)
                continue

            batch_count += 1

            df = pd.DataFrame(candles)
            df.rename(columns={
                "date": "timestamp",
                "open": "open",
                "high": "high",
                "low": "low",
                "close": "close",
                "volume": "volume"
            }, inplace=True)

            insert_ohlcv(df, token)  # ✅ Call your new ingest logic

            row_count = len(df)
            print(f"✅ {symbol}: {from_date.date()} → {to_date.date()} | {row_count} rows")
            total_inserted += row_count
            start_date = to_date + datetime.timedelta(days=1)

            time.sleep(SLEEP_BETWEEN_CALLS)

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Too many requests" in error_msg:
                print(f"❌ {symbol}: Error Too many requests → waiting 15s and retrying...")
                time.sleep(15)
            elif "token is invalid" in error_msg:
                print(f"❌ {symbol}: Invalid access token.")
                break
            else:
                print(f"❌ {symbol}: Error {error_msg}")
                start_date += datetime.timedelta(days=RETRY_INCREMENT_DAYS)

    print(f"\n🎯 {symbol}: Total inserted: {total_inserted}")
    return {
        "symbol": symbol,
        "rows": total_inserted,
        "start": START_DATE.strftime("%Y-%m-%d"),
        "end": END_DATE.strftime("%Y-%m-%d")
    }

# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────

def print_summary(summary_list):
    print("\n📊 Summary Report:")
    for s in summary_list:
        print(f"• {s['symbol']}: {s['rows']} rows from {s['start']} to {s['end']}")

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    summary = []
    for item in INDEX_INSTRUMENTS:
        result = fetch_ohlcv(item["token"], item["symbol"])
        summary.append(result)

    print_summary(summary)
