import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that opens a database connection, 
    passes it to the wrapped function, and ensures it closes afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# 🔍 Test connection handling
user = get_user_by_id(user_id=1)
print(user)
