import mysql.connector
from mysql.connector import Error

# Define database connection parameters
DB_PARAMS = {
    'database': 'aminet',
    'user': 'root',
    'password': 'JKLÇnm,.0',  # Replace with your actual password
    'host': '127.0.0.1',
    'port': '3306'
}

def connect_db():
    """Establish and return a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_PARAMS)
        if conn.is_connected():
            print("Connection successful!")
            return conn
        else:
            print("Failed to connect.")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None

def main():
    """Main function to test database connection."""
    connection = connect_db()
    if connection:
        connection.close()

if __name__ == "__main__":
    main()
