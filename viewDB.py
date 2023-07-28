import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("SELECT * FROM users")

for row in cur:
    print(row)

conn.close()
