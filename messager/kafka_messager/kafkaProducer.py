import datetime
import time
from decimal import Decimal
from fullstack_backend_itp24109.messager.sources.neo4j_source import Neo4jDataSource
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
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, frozenset):  # For Neo4j labels
            return list(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    @staticmethod
    def process_neo4j_data(data):
        """Process Neo4j data to a serializable format."""
        processed_data = []

        for item in data:
            user_node = item['user']  # Node representing the main user
            related_user_node = item['related_user']  # Node representing the related user
            relationship = item['relationship']  # Relationship object

            # Extract user and relationship details
            user_data = user_node._properties  # All properties of the user node
            related_user_id = related_user_node['userID']  # Related user's ID
            relationship_type = relationship.type  # Type of the relationship

            # Find if the user already exists in the processed data
            existing_entry = next((entry for entry in processed_data if entry['userID'] == user_data['userID']), None)

            # If user already exists, append to their relationships
            if existing_entry:
                existing_entry['relationships'].append({
                    'related_userID': related_user_id,
                    'relationship_type': relationship_type
                })
            else:
                # Add new user entry with relationships
                user_entry = {
                    **user_data,  # Include all user properties
                    "relationships": [
                        {
                            "related_userID": related_user_id,
                            "relationship_type": relationship_type
                        }
                    ]
                }
                processed_data.append(user_entry)
        
        return processed_data

    def produce(self):
        """Fetch data from the data source and publish to Kafka."""
        print(f"Producing data to Kafka topic: {self.topic}")
        data = self.data_source.fetch_data(self.rate_limit)
        if isinstance(self.data_source, Neo4jDataSource):
            data = KafkaProducerImpl.process_neo4j_data(data)
        try:
            for item in data:
                node_data = dict(item)  # Extract properties as a dictionary
                serialized_data = json.dumps(node_data, default=KafkaProducerImpl.json_serial).encode()
                self.producer.send(self.topic, serialized_data)
            self.producer.flush()
        except Exception as e:
            print(f"Error producing data to Kafka: {e}")
 
    def run_and_sleep(self):
        """Run the producer and sleep for a specified interval."""
        self.produce()
        time.sleep(self.time_interval)
        self.run_and_sleep()