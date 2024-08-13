import mysql.connector
from mysql.connector import Error

DB_PARAMS ={
    'database': 'aminet',
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'port': '3306'
}

def connect_db():
    """Establish and return a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_PARAMS)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None