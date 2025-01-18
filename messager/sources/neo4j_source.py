from neo4j import GraphDatabase
from source import DataSource

class Neo4jDataSource(DataSource):
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    async def fetch_data(self) -> list:
        """Fetch data from Neo4j."""
        session = self.driver.session()
        query = "MATCH (u:User) RETURN u LIMIT 10;"
        result = session.run(query)
        users = []
        for record in result:
            user_data = record["u"]
            users.append({
                "id": user_data.id,
                "connections": [conn.id for conn in user_data.relationships]
            })
        session.close()
        return users
