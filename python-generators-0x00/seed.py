import mysql.connector
import csv
import os
from mysql.connector import errorcode

def connect_db():
    """Connects to the MySQL database server."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
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
            password="",
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
                age DECIMAL(5,2) NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")

def insert_data(connection, csv_path):
    print(f"Looking for CSV file at: {csv_path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"File exists: {os.path.isfile(csv_path)}")
    try:
        cursor = connection.cursor()
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row['user_id'], row['name'], row['email'], float(row['age'])))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Data insert failed: {err}")
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
    except KeyError as e:
        print(f"CSV file missing required column: {e}")