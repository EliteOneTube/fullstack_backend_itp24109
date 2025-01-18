from neo4j import GraphDatabase
from source import DataSource

class Neo4jDataSource(DataSource):
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def fetch_data(self, rate_limit: int) -> list:
        """Fetch data from Neo4j."""
        session = self.driver.session()
        query = """
        MATCH (u:User)
        OPTIONAL MATCH (u)-[r]->()
        RETURN u, r LIMIT %s
        """ % rate_limit  # Adjusted query with OPTIONAL MATCH to handle users without relationships
        result = session.run(query)
        users = []

        for record in result:
            user_data = record["u"]
            relationships = record["r"] if record["r"] else []  # Handle the case where there might be no relationships
            users.append({
                "id": user_data.id,
                "connections": [rel.id for rel in relationships]
            })

        session.close()
        return users
