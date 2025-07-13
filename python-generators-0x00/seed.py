import mysql.connector
import csv
import uuid
from mysql.connector import errorcode

def connect_db():
    """Connects to the MySQL database server."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password@123",  # Replace with the password you used in CMD
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password@123",  # Match the password from connect_db
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")

def insert_data(connection, csv_path):
    """Inserts data into the user_data table from a CSV file."""
    try:
        cursor = connection.cursor()
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Data insert failed: {err}")
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")

def stream_user_data(connection):
    """Generator to stream rows from user_data table one by one."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()