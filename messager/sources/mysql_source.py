import mysql.connector
from source import DataSource

class MySQLDataSource(DataSource):
    def __init__(self, host: str, user: str, password: str, database: str):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)
        self.start_position = 0

    def fetch_data(self, rate_limit: int) -> list:
        """Fetch data from MySQL starting from a specific position."""
        query = "SELECT * FROM clothes WHERE clothID > %s ORDER BY clothID ASC LIMIT %s" % (self.start_position, rate_limit)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.start_position += rate_limit
        return result
