import sqlite3
import functools

def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.
    Assumes the wrapped function takes 'query' as its first argument or keyword.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try getting 'query' from kwargs first, then fallback to args[0]
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Test execution
users = fetch_all_users(query="SELECT * FROM users")
print(users)