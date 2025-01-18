import asyncio
import json
from kafka import KafkaConsumer
from pymongo import MongoClient


class KafkaConsumerHandler:
    def __init__(self, kafka_brokers: str, mongo_uri: str, mongo_db: str, mongo_collection: str):
        self.kafka_brokers = kafka_brokers
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_collection = self.mongo_client[mongo_db][mongo_collection]
        self.consumer = None

    def connect(self) -> None:
        """Connect the Kafka consumer to the specified topic."""
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.kafka_brokers,
            auto_offset_reset='earliest',
            group_id='fusion_group',
            enable_auto_commit=True
        )

    def consume(self) -> None:
        """Start consuming messages from Kafka."""
        if not self.consumer:
            raise RuntimeError("Kafka consumer is not connected to any topic.")
        
        print("Starting to consume messages...")
        for message in self.consumer:
            try:
                print(f"Received message: {message}")
                if "clothes" in message and "users" in message:
                    # Perform data fusion
                    fused_data = {
                        "clothesID": message["clothes"]["id"],
                        "style": message["clothes"]["style"],
                        "price": message["clothes"]["price"],
                        "userID": message["users"]["id"],
                        "connections": message["users"]["connections"],
                    }
                    # Store the fused data in MongoDB
                    self.mongo_collection.insert_one(fused_data)
                    print(f"Fused data inserted: {fused_data}")
                else:
                    print(f"Invalid message: {message}")
            except Exception as e:
                print(f"Error handling message: {e}")
        
    def disconnect(self) -> None:
        """Disconnect the Kafka consumer."""
        if self.consumer:
            self.consumer.close()
            print("Kafka consumer disconnected.")