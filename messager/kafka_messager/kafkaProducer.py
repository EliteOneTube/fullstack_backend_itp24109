import time
from decimal import Decimal
from kafka import KafkaProducer
import json
from source import DataSource

class KafkaProducerImpl:
    """A universal Kafka producer."""
    def __init__(self, brokers: str, topic: str, data_source: DataSource, rate_limit: int, time_interval: int):
        """
        Args:
            brokers (str): Kafka broker addresses.
            topic (str): Kafka topic to publish to.
            data_source (DataSource): Data source providing the data.
            rate_limit (int): Number of messages per interval.
            time_interval (int): Time interval to sleep after each interval.
        """
        self.brokers = brokers
        self.topic = topic
        self.data_source = data_source
        self.rate_limit = rate_limit
        self.producer = KafkaProducer(
            bootstrap_servers=brokers                            
        )
        self.time_interval = time_interval

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default."""
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")


    def produce(self):
        """Fetch data from the data source and publish to Kafka."""
        print(f"Producing data to Kafka topic: {self.topic}")
        data = self.data_source.fetch_data(self.rate_limit)
        for item in data:
            # Use the custom serializer
            serialized_data = json.dumps(item, default=KafkaProducerImpl.json_serial).encode()
            self.producer.send(self.topic, serialized_data)
        self.producer.flush()
 
    def run_and_sleep(self):
        """Run the producer and sleep for a specified interval."""
        self.produce()
        time.sleep(self.time_interval)
        self.run_and_sleep()