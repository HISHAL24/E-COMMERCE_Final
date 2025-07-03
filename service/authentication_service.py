# service/authentication_service.py

import mysql.connector

class AuthenticationService:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shaa@9846",
            database="catalogue_dbms"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def validate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        return result is not None
