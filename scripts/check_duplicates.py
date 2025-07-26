from backend.db.connection import get_db_connection


def find_duplicates():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT instrument_token, timestamp, COUNT(*)
        FROM ohlcv
        GROUP BY instrument_token, timestamp
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        """
    )
    rows = cur.fetchall()
    if not rows:
        print("✅ No duplicates found.")
    else:
        for token, ts, count in rows:
            print(f"Duplicate: token={token} ts={ts} count={count}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    find_duplicates()
