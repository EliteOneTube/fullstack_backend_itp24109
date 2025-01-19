from neo4j import GraphDatabase
from source import DataSource

class Neo4jDataSource(DataSource):
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def fetch_data(self, rate_limit: int) -> list:
        """Fetch data from Neo4j."""
        query = f"""
        MATCH (n)
        RETURN n
        LIMIT {rate_limit}
        """
        with self.driver.session() as session:  # Use 'with' to ensure session closure
            result = session.run(query)
            records = [record["n"] for record in result]  # Extract nodes from the query result
        return records
