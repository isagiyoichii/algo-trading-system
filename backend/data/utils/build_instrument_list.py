import os
import psycopg2
from dotenv import load_dotenv
from backend.db.connection import get_pg_connection

# ─────────────────────────────
# 🔧 ENVIRONMENT SETUP
# ─────────────────────────────
# Fix: Point to project root (algo-trading-system/)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

OUTPUT_PATH = os.path.join(ROOT_DIR, "backend", "data", "utils", "instrument_list.py")

# ─────────────────────────────
# 🔄 FORMAT SINGLE ENTRY
# ─────────────────────────────
def format_entry(row):
    token, symbol = row
    return f'    {{"token": {token}, "symbol": "{symbol}"}}'

# ─────────────────────────────
# 📥 FETCH & CATEGORIZE
# ─────────────────────────────
def fetch_and_group_instruments():
    conn = get_pg_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT instrument_token, tradingsymbol, segment, instrument_type, expiry
        FROM instruments
        WHERE tradingsymbol IS NOT NULL
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    index_list = []
    equity_list = []
    future_list = []

    for row in rows:
        token, symbol, segment, inst_type, expiry = row
        if segment == "INDICES":
            index_list.append((token, symbol))
        elif inst_type == "EQ":
            equity_list.append((token, symbol))
        elif inst_type == "FUT" and segment and "FUT" in segment:
            future_list.append((token, symbol))

    return index_list, equity_list, future_list

# ─────────────────────────────
# ✍️ WRITE OUTPUT FILE
# ─────────────────────────────
def write_python_file(index, equity, future):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🔧 Auto-generated instrument list from instruments table\n\n")

        f.write("INDEX_INSTRUMENTS = [\n")
        f.write(",\n".join([format_entry(row) for row in index]))
        f.write("\n]\n\n")

        f.write("EQUITY_INSTRUMENTS = [\n")
        f.write(",\n".join([format_entry(row) for row in equity]))
        f.write("\n]\n\n")

        f.write("FUTURE_INSTRUMENTS = [\n")
        f.write(",\n".join([format_entry(row) for row in future]))
        f.write("\n]\n")

    print(f"✅ instrument_list.py generated with {len(index)} indices, {len(equity)} equities, {len(future)} futures.")

# ─────────────────────────────
# 🏁 RUN
# ─────────────────────────────
if __name__ == "__main__":
    idx, eq, fut = fetch_and_group_instruments()
    write_python_file(idx, eq, fut)
    