import sqlite3

# Connect to the database (will create 'users.db' if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
""")

# Optionally insert sample data
cursor.execute("INSERT INTO users (name, email) VALUES ('Portia Mashaba', 'portia@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Nelisiwe N.', 'nelisiwe@example.com')")

conn.commit()
conn.close()

print("users table created and seeded ✅")
