import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Print the current schema
cursor.execute("PRAGMA table_info(notifications_notification)")
columns = cursor.fetchall()
print("Current columns:")
for column in columns:
    print(column)

try:
    # Add the url column if it doesn't exist
    cursor.execute("ALTER TABLE notifications_notification ADD COLUMN url varchar(255) DEFAULT ''")
    conn.commit()
    print("Column 'url' added successfully")
    
    # Check the schema again
    cursor.execute("PRAGMA table_info(notifications_notification)")
    columns = cursor.fetchall()
    print("\nUpdated columns:")
    for column in columns:
        print(column)
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
    conn.rollback()

conn.close()
print("Database connection closed") 