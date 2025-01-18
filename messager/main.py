import asyncio
from kafka_messager.kafkaProducer import KafkaProducerImpl
from kafka_messager.kafkaConsumer import KafkaConsumerHandler
from sources.mysql_source import MySQLDataSource
from sources.neo4j_source import Neo4jDataSource
from concurrent.futures import ThreadPoolExecutor
from kafka.admin import NewTopic
from kafka import KafkaAdminClient

async def main():
    # MySQL Data Source
    mysql_source = MySQLDataSource(host="mysql", user="root", password="rootpassword", database="ClothingStore")
    mysql_topic = "clothes-topic"

    # Neo4j Data Source
    neo4j_source = Neo4jDataSource(uri="bolt://neo4j:7687", user="neo4j", password="password")
    neo4j_topic = "users-topic"

    # Create Kafka topics
    admin_client = KafkaAdminClient(bootstrap_servers="kafka:9092")
    admin_client.create_topics([
        NewTopic(name=mysql_topic, num_partitions=1, replication_factor=1),
        NewTopic(name=neo4j_topic, num_partitions=1, replication_factor=1)
    ])

    # Universal Kafka Producers
    mysql_producer = KafkaProducerImpl(
        brokers="kafka:9092",
        topic=mysql_topic,
        data_source=mysql_source,
        rate_limit=10,  # Publish 10 messages per interval
        time_interval=10  # Sleep for 5 seconds after each interval
    )
    neo4j_producer = KafkaProducerImpl(
        brokers="kafka:9092",
        topic=neo4j_topic,
        data_source=neo4j_source,
        rate_limit=5,  # Publish 5 messages per interval
        time_interval=20  # Sleep for 10 seconds after each interval
    )

    # Kafka Consumer for Data Fusion
    kafka_consumer = KafkaConsumerHandler(
        kafka_brokers="kafka:9092",
        mongo_uri="mongodb://localhost:27017/",
        mongo_db="fusion_db",
        mongo_collection="fused_data"
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
