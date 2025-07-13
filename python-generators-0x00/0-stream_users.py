import mysql.connector

def stream_users():
    """Generator to stream rows from the user_data table one by one."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data')
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return