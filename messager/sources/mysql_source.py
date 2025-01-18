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

    async def fetch_data(self) -> list:
        """Fetch data from MySQL."""
        query = "SELECT * FROM clothes LIMIT 10;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
