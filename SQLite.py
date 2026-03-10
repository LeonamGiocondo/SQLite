# Creating an SQLite database
# The central idea here is: to store data in a structured way (tables), with rules (constraints) and relationships (foreign keys), and manipulate everything via SQL, using Python as a #"client" of the database.


import sqlite3
from pathlib import Path

DB_FILE = Path("store.db")

SCHEMA = """
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  date TEXT NOT NULL,          -- formate ISO: YYYY-MM-DD
  total REAL NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
"""

CUSTOMER = [
    (1, "Ana", "São Paulo"),
    (2, "Bruno", "Rio de Janeiro"),
    (3, "Carla", "Belo Horizonte"),
    (4, "Diego", "São Paulo"),
]

ORDERS = [
    (1, 1, "2026-01-10", 120.50),
    (2, 1, "2026-02-03", 89.90),
    (3, 2, "2026-02-10", 45.00),
    (4, 3, "2026-03-01", 250.00),
]

def main():
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        cur.executescript(SCHEMA)
        cur.executemany("INSERT INTO customer (id, name, city) VALUES (?, ?, ?);", CUSTOMER)
        cur.executemany("INSERT INTO orders (id, customer_id, date, total) VALUES (?, ?, ?, ?);", ORDERS)
        conn.commit()
        print(f"Bank created successfully: {DB_FILE.resolve()}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()


