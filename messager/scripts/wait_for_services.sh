#!/bin/bash

# Check MySQL
echo "Waiting for MySQL..."
until nc -z -v -w30 $MYSQL_HOST $MYSQL_PORT
do
  echo "Waiting for MySQL connection..."
  sleep 5
done

# Check Neo4j
echo "Waiting for Neo4j..."
until nc -z -v -w30 neo4j 7687
do
  echo "Waiting for Neo4j connection..."
  sleep 5
done

# Check MongoDB
echo "Waiting for MongoDB..."
until nc -z -v -w30 mongodb 27017
do
  echo "Waiting for MongoDB connection..."
  sleep 5
done

# Check Kafka
echo "Waiting for Kafka..."
until nc -z -v -w30 kafka 9092
do
  echo "Waiting for Kafka connection..."
  sleep 5
done

echo "All services are up and ready!"

# Once the services are ready, start the main application
python ../main.py
