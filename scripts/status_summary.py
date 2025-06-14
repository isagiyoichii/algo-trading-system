# scripts/status_summary.py

import psycopg2
from backend.db.connection import get_db_connection
from backend.data.utils.instrument_list import SELECTED_INDICES

def generate_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    print(f"{'Instrument':<30} {'Token':<10} {'Start Date':<22} {'End Date':<22} {'Rows':<10}")
    print("-" * 100)

    for index in SELECTED_INDICES:
        token = index['instrument_token']
        name = index['name']

        cursor.execute("""
            SELECT MIN(timestamp), MAX(timestamp), COUNT(*)
            FROM ohlcv
            WHERE instrument_token = %s
        """, (token,))

        result = cursor.fetchone()
        if result[2] > 0:
            print(f"{name:<30} {token:<10} {str(result[0]):<22} {str(result[1]):<22} {result[2]:<10}")
        else:
            print(f"{name:<30} {token:<10} {'No Data':<22} {'No Data':<22} 0")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    generate_summary()
