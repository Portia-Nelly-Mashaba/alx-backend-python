import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to stream rows from the user_data table in batches."""
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
            batch = []
            for _ in range(batch_size):
                row = cursor.fetchone()
                if row is None:
                    break
                batch.append(row)
            if not batch:
                break
            yield batch
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def batch_processing(batch_size):
    """Generator to process batches and yield users over 25 years old."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user