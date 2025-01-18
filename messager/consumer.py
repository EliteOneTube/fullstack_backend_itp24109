from abc import ABC, abstractmethod

class AbstractConsumer(ABC):
    @abstractmethod
    def consume(self) -> None:
        """Start consuming messages."""
        pass

    @abstractmethod
    async def handle(self, payload: dict) -> None:
        """Handle a single message payload.

        Args:
            payload (dict): The message payload to process.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect the consumer."""
        pass

    @abstractmethod
    def connect(self, topic: str) -> None:
        """Connect the consumer to a specific topic.

        Args:
            topic (str): The topic to subscribe to.
        """
        pass
