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
            try:
                message_value = json.loads(message.value)  # Assuming JSON encoding for Kafka messages
                print(message.topic)
                if message.topic == 'clothes-topic':
                    # Insert data into 'clothes' collection
                    clothe_id = message_value.get('clothID')
                    if clothe_id is None:
                        continue  # Skip this message if no clotheID is found

                    existing_clothe = self.mongo_db['clothes'].find_one({'clothID': clothe_id})

                    if existing_clothe:
                        continue  # Skip this message if clothe already exists

                    self.mongo_db['clothes'].insert_one(message_value)
                elif message.topic == 'users-topic':
                    user_id = message_value.get('userID')
                    if user_id is None:
                        continue  # Skip this message if no userID is found

                    existing_user = self.mongo_db['users'].find_one({'userID': user_id})

                    if existing_user:
                        self.mongo_db['users'].update_one(
                            {'userID': user_id},
                            {
                                '$addToSet': {
                                    'relationships': {'$each': message_value.get('relationships', [])},
                                    'purchased': {'$each': message_value.get('purchased', [])}
                                }
                            }
                        )
                    else:
                        self.mongo_db['users'].insert_one(message_value)

            except json.JSONDecodeError as e:
                pass
            except Exception as e:
                pass