#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """Generator to stream user ages one by one from the user_data table."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT age FROM user_data')
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row['age']
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def calculate_average_age():
    """Calculate and print the average age using the stream_user_ages generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")

if __name__ == "__main__":
    calculate_average_age()