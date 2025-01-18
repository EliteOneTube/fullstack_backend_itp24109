from producer import AbstractProducer
from kafka import KafkaProducer
import json
import asyncio
from source import DataSource

class KafkaProducerImpl(AbstractProducer):
    def __init__(self, bootstrap_servers: str):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        """Start the Kafka producer."""
        pass  # Kafka producer starts automatically when sending messages

    async def send_and_wait(self, topic: str, message: bytes):
        """Send a message to the Kafka topic."""
        print(f"Sending message to topic: {topic}")
        self.producer.send(topic, message)
        self.producer.flush()  # Ensure the message is sent

    async def stop(self):
        """Stop the producer."""
        self.producer.close()

class UniversalKafkaProducer:
    """A universal Kafka producer."""
    def __init__(self, brokers: str, topic: str, data_source: DataSource, rate_limit: int, producer: KafkaProducerImpl):
        """
        Args:
            brokers (str): Kafka broker addresses.
            topic (str): Kafka topic to publish to.
            data_source (DataSource): Data source providing the data.
            rate_limit (int): Number of messages per interval.
            producer (AbstractProducer): Kafka producer implementation.
        """
        self.brokers = brokers
        self.topic = topic
        self.data_source = data_source
        self.rate_limit = rate_limit
        self.producer = producer

    async def produce(self, interval: int):
        """Fetch data from the data source and publish to Kafka."""
        await self.producer.start()
        try:
            while True:
                data = await self.data_source.fetch_data()
                for item in data[:self.rate_limit]:
                    await self.producer.send_and_wait(self.topic, json.dumps(item).encode('utf-8'))
                await asyncio.sleep(interval)
        finally:
            await self.producer.stop()