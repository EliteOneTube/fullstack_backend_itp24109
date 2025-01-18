from producer import AbstractProducer
from kafka import KafkaProducer
import json
import asyncio
from source import DataSource

class KafkaProducerImpl(AbstractProducer):
    """A universal Kafka producer."""
    def __init__(self, brokers: str, topic: str, data_source: DataSource, rate_limit: int):
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
        self.producer = KafkaProducer(bootstrap_servers=brokers)

    async def produce(self, interval: int):
        """Fetch data from the data source and publish to Kafka."""
        print(f"Producing data to Kafka topic: {self.topic}")
        # try:
        #     print("Starting Kafka producer...")
        #     while True:
        #         print("Fetching data...")
        #         data = await self.data_source.fetch_data(self.rate_limit)
        #         for item in data[:self.rate_limit]:
        #             print(f"Publishing message: {item}")
        #             self.producer.send(self.topic, json.dumps(item).encode())
        #         self.producer.flush()
        #         await asyncio.sleep(interval)
        # finally:
        #     await self.producer.stop()

    async def start(self):
        """Start the Kafka producer."""
        pass  # Kafka producer starts automatically when sending messages
        

    async def stop(self):
        """Stop the producer."""
        self.producer.close()