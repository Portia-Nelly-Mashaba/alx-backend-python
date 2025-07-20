import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """
    Opens a SQLite connection and passes it to the wrapped function.
    Ensures the connection is properly closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Caches query results based on the SQL query string.
    If the same query is repeated, returns cached result instead of hitting the database.
    """
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]
        print(f"[CACHE MISS] Executing and caching query: {query}")
        result = func(conn, query)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# 🔍 First call — result gets cached
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# 🔁 Second call — returns from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
