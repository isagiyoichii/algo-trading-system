from pathlib import Path
from backend.db.connection import get_pg_connection

def initialize_schema():
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database schema initialized")

if __name__ == "__main__":
    initialize_schema()
