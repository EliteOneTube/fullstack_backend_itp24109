from neo4j import GraphDatabase
from source import DataSource

class Neo4jDataSource(DataSource):
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.start_position = 0
    
    def fetch_data(self, rate_limit: int) -> list:
        """Fetch data from Neo4j."""
        query = f"""
        MATCH (u:User)-[r]->(v)
        RETURN u, r, v
        SKIP {self.start_position}
        LIMIT {rate_limit}
        """
        with self.driver.session() as session:  # Use 'with' to ensure session closure
            result = session.run(query)
            records = [{"user": record["u"], "relationship": record["r"], "related_user": record["v"]} for record in result]  # Extract users and their relationships from the query result
        self.start_position += rate_limit  # Increase start position by rate limit
        print(f"Fetched {records} records from Neo4j.")
        return records
