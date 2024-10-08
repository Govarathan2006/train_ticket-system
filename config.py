import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Govarathan@2006',
            database='ticket_system'
        )
        if conn.is_connected():
            print("Connected to MySQL database")
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
connection = get_db_connection()

if connection:
    cursor = connection.cursor()  # Only proceed if connection is successful
    # Perform your database operations here
else:
    print("Connection to the database failed. Cannot proceed.")
