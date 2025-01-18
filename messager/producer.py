# producer.py

from abc import ABC, abstractmethod

class AbstractProducer(ABC):
    @abstractmethod
    async def start(self):
        """Start the producer."""
        pass

    @abstractmethod
    async def send_and_wait(self, topic: str, message: bytes):
        """Send a message to the Kafka topic."""
        pass

    @abstractmethod
    async def stop(self):
        """Stop the producer."""
        pass
