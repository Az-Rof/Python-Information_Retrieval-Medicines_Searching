import mysql.connector


class DatabaseConnection:
    def __init__(self, user='root', password='', host='localhost', database='medicine'):
        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database,
        }
        try:
            self.db_connect = mysql.connector.connect(**config)
            self.cursor = self.db_connect.cursor()
            print("Database connected successfully")
        except mysql.connector.Error as err:
            print("Database connection failed:", err)
            self.db_connect = None
            self.cursor = None

    def select(self, query, params=None):
        if self.cursor:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        return []

    def execute(self, query, params=None):
        if self.cursor:
            self.cursor.execute(query, params or ())
            self.db_connect.commit()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db_connect:
            self.db_connect.close()
