from abc import ABC, abstractmethod

class DataSource(ABC):
    """Abstract class for data sources like MySQL, Neo4j."""
    @abstractmethod
    async def fetch_data(self) -> list:
        """Fetch data to be published to Kafka."""
        pass