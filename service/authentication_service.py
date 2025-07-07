# service/authentication_service.py

import logging
import mysql.connector

logger = logging.getLogger(__name__)

class AuthenticationService:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shaa@9846",
                database="catalogue_dbms"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            logger.info("Database connection for AuthenticationService established successfully.")
        except mysql.connector.Error as err:
            logger.exception("Error connecting to the database in AuthenticationService")
            raise

    def validate_user(self, username, password):
        logger.debug(f"Validating user with username: {username}")
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            if result:
                logger.info(f"User '{username}' authenticated successfully.")
                return True
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return False
        except Exception as e:
            logger.exception(f"Exception occurred while validating user: {username}")
            raise

