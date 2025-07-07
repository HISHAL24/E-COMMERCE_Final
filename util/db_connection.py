"""
Utility module to provide database connection.
"""

import logging
import mysql.connector
from mysql.connector import Error

logger = logging.getLogger(__name__)

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
            logger.info("Database connection established successfully.")
            return conn
        else:
            logger.error("Database connection failed.")
            return None
    except Error as e:
        logger.exception(f"Error connecting to database: {e}")
        return None

