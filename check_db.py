import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Get table info for notifications_notification
print("\nColumns in notifications_notification table:")
try:
    cursor.execute("PRAGMA table_info(notifications_notification)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"Column ID: {column[0]}, Name: {column[1]}, Type: {column[2]}, NotNull: {column[3]}, Default: {column[4]}, PK: {column[5]}")
except Exception as e:
    print(f"Error: {e}")

conn.close() 