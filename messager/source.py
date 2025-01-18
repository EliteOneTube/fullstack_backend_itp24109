from abc import ABC, abstractmethod

class DataSource(ABC):
    """Abstract class for data sources like MySQL, Neo4j."""
    @abstractmethod
    async def fetch_data(self, rate_limit: int) -> list:
        """Fetch data to be published to Kafka."""
        pass