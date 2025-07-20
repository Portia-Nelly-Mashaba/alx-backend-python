import time
import sqlite3
import functools

def with_db_connection(func):
    """
    Opens a SQLite connection and passes it to the wrapped function.
    Ensures the connection is closed afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Retries a function on failure due to exceptions.
    Useful for handling transient errors in database operations.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"[Retry {attempt}] Error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            print(f"[FAILED] All {retries} attempts exhausted.")
            raise Exception("Operation failed after retries")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# 🔍 Attempt to fetch users with retry logic
users = fetch_users_with_retry()
print(users)
