import asyncio
from kafka_messager.kafkaProducer import KafkaProducerImpl
from kafka_messager.kafkaConsumer import KafkaConsumerHandler
from sources.mysql_source import MySQLDataSource
from sources.neo4j_source import Neo4jDataSource
from concurrent.futures import ThreadPoolExecutor
from kafka.admin import NewTopic
from kafka import KafkaAdminClient
import os

async def main():
    # Kafka
    kafka_brokers = os.getenv("KAFKA_BROKERS")

    # MongoDB Data Source
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DATABASE")

    # Neo4j Data Source
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    # MySQL Data Source
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_database = os.getenv("MYSQL_DATABASE")

    # MySQL Data Source
    mysql_source = MySQLDataSource(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)
    mysql_topic = "clothes-topic"

    # Neo4j Data Source
    neo4j_source = Neo4jDataSource(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
    neo4j_topic = "users-topic"

    # Create Kafka topics
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=kafka_brokers)
        admin_client.create_topics([
            NewTopic(name=mysql_topic, num_partitions=1, replication_factor=1),
            NewTopic(name=neo4j_topic, num_partitions=1, replication_factor=1)
        ])
    except Exception as e:
        pass

    # Universal Kafka Producers
    mysql_producer = KafkaProducerImpl(
        brokers=kafka_brokers,
        topic=mysql_topic,
        data_source=mysql_source,
        rate_limit=10,
        time_interval=10
    )
    neo4j_producer = KafkaProducerImpl(
        brokers=kafka_brokers,
        topic=neo4j_topic,
        data_source=neo4j_source,
        rate_limit=5,
        time_interval=20 
    )

    # Kafka Consumer for Data Fusion
    kafka_consumer = KafkaConsumerHandler(
        kafka_brokers=kafka_brokers,
        mongo_uri=mongo_uri,
        mongo_db=mongo_db,
        mongo_collections=["clothes", "users"]
    )

    # Connect Kafka Consumer to the topics
    kafka_consumer.connect()

    kafka_consumer.consumer.subscribe([mysql_topic, neo4j_topic])

    # Start the Kafka Consumer and Producers in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        loop = asyncio.get_event_loop()
        # Schedule all tasks concurrently
        await asyncio.gather(
            loop.run_in_executor(executor, kafka_consumer.consume),
            loop.run_in_executor(executor, mysql_producer.run_and_sleep),
            loop.run_in_executor(executor, neo4j_producer.run_and_sleep),
        )

if __name__ == "__main__":
    asyncio.run(main())
