# Learn SQL with a simple “executor”

import sqlite3
from pathlib import Path

DB_FILE = Path("store.db")

def main():
    sql = input("Paste your SQL query and press Enter.:\n> ").strip()
    if not sql:
        print("Empty query.")
        return

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        if not rows:
            print("0 Returned rows.")
            return

        # print columns
        cols = rows[0].keys()
        print(" | ".join(cols))
        print("-" * (3 * len(cols) + 10))

        for r in rows:
            print(" | ".join(str(r[c]) for c in cols))
    finally:
        conn.close()

if __name__ == "__main__":
    main()
