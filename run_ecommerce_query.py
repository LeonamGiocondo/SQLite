# Querys 


# Import and initial setup
import sqlite3

DB_NAME = "ecommerce.db"

# User interface
print("=== CONSULTATION SQL - ECOMMERCE ===")
print("Enter your SQL query.")
print("When you are finished, type END on a new line.\n")

lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    lines.append(line)

query = "\n".join(lines).strip()

# Empty query check
if not query:
    print("None query were typed.")
    exit()

# SQL query execution
try:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(query)

# SQL query processing
    if query.lower().startswith("select"):
        rows = cursor.fetchall()

        if rows:
            columns = rows[0].keys()

            col_widths = {}
            for col in columns:
                max_len = len(col)
                for row in rows:
                    max_len = max(max_len, len(str(row[col])))
                col_widths[col] = max_len

            header = " | ".join(f"{col:<{col_widths[col]}}" for col in columns)
            separator = "-+-".join("-" * col_widths[col] for col in columns)

            print("\n" + header)
            print(separator)

            for row in rows:
                print(" | ".join(f"{str(row[col]):<{col_widths[col]}}" for col in columns))

            print(f"\nTotal lines: {len(rows)}")
        else:
            print("\nNo results found.")
    # Handling Other Queries (INSERT, UPDATE, DELETE)
    else:
        conn.commit()
        print("\nQuery successfully executed!")

except Exception as e:
    print(f"\nError when executing query: {e}")

finally:
    conn.close()
