import asyncio
from kafka_messager.kafkaProducer import KafkaProducerImpl
from kafka_messager.kafkaConsumer import KafkaConsumerHandler
from sources.mysql_source import MySQLDataSource
from sources.neo4j_source import Neo4jDataSource
import sched, time

async def main():
    # MySQL Data Source
    mysql_source = MySQLDataSource(host="mysql", user="root", password="rootpassword", database="ClothingStore")
    mysql_topic = "clothes-topic"

    # Neo4j Data Source
    neo4j_source = Neo4jDataSource(uri="bolt://localhost:7687", user="neo4j", password="password")
    neo4j_topic = "users-topic"

    # Universal Kafka Producers
    mysql_producer = KafkaProducerImpl(
        brokers="localhost:9092",
        topic=mysql_topic,
        data_source=mysql_source,
        rate_limit=10  # Publish 10 messages per interval
    )
    neo4j_producer = KafkaProducerImpl(
        brokers="localhost:9092",
        topic=neo4j_topic,
        data_source=neo4j_source,
        rate_limit=5  # Publish 5 messages per interval
    )

    # Kafka Consumer for Data Fusion
    kafka_consumer = KafkaConsumerHandler(
        kafka_brokers="kafka:9092",
        mongo_uri="mongodb://localhost:27017/",
        mongo_db="fusion_db",
        mongo_collection="fused_data"
    )

    s = sched.scheduler(time.time, time.sleep)

    # Connect Kafka Consumer to the topics
    kafka_consumer.connect(mysql_topic)
    kafka_consumer.connect(neo4j_topic)

    # Run Producers and Consumer concurrently
    s.enter(1, 1, mysql_producer.produce)
    s.enter(1, 1, neo4j_producer.produce)

    s.run()

    kafka_consumer.consume()


if __name__ == "__main__":
    asyncio.run(main())
