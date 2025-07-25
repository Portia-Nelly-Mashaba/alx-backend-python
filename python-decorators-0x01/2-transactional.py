import sqlite3
import functools

def with_db_connection(func):
    """
    Opens a database connection and passes it to the wrapped function.
    Closes the connection after the function executes.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Wraps a database operation in a transaction.
    Commits if successful, rolls back if an error occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction failed: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# 🔍 Call the update function
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
