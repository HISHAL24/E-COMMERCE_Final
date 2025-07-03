"""
Utility module to provide database connection.
"""

import mysql.connector
from mysql.connector import Error

def get_connection():
    """Establish and return a database connection."""

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shaa@9846",
            database="catalogue_dbms"
        )
        if conn.is_connected():
            return conn
        else:
            print("Connection failed.")
            return None
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
