import asyncio
import json
from kafka import KafkaConsumer
from pymongo import MongoClient


class KafkaConsumerHandler:
    def __init__(self, kafka_brokers: str, mongo_uri: str, mongo_db: str, mongo_collections: list[str]):
        self.kafka_brokers = kafka_brokers
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.consumer = None
        self.mongo_collections = mongo_collections

        # Create MongoDB collections
        for collection in mongo_collections:
            if collection not in self.mongo_db.list_collection_names():
                self.mongo_db.create_collection(collection)

    def connect(self) -> None:
        """Connect the Kafka consumer to the specified topic."""
        self.consumer = KafkaConsumer(
            'fusion-topic',
            bootstrap_servers=self.kafka_brokers,
            auto_offset_reset='earliest',
            group_id='fusion_group',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume(self) -> None:
        """Start consuming messages from Kafka."""
        if not self.consumer:
            raise RuntimeError("Kafka consumer is not connected to any topic.")
        
        print("Starting to consume messages...")
        for message in self.consumer:
            #If the topic is 'clothes-topic', insert the data into the MongoDB collection 'clothes', else insert into 'users'
            if message.topic == 'clothes-topic':
                self.mongo_db['clothes'].insert_one(message.value)
            elif message.topic == 'users-topic':
                user_id = message.value.get('userID')
                existing_user = self.mongo_db['users'].find_one({'userID': user_id})
                
                if existing_user:
                    # Update the existing user with new relationships and products bought
                    self.mongo_db['users'].update_one(
                        {'userID': user_id},
                        {
                            '$addToSet': {
                                'relationships': {'$each': message.value.get('relationships', [])},
                                'purchased': {'$each': message.value.get('products_bought', [])}
                            }
                        }
                    )
                else:
                    # Insert new user document
                    self.mongo_db['users'].insert_one(message.value)