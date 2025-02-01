# Extract Transform Load Procedure

## Tech Stack

**Server:** Flask (Python)

**Database:** MongoDB, Neo4j, MySQL

**Messaging**: Kafka

## Environment Variables

### Configuration

Before running the application, you **must configure** the environment variables.

1. Rename `template.env` to `.env`.
2. Update the values inside `.env` as needed to match your setup.

Docker Compose will automatically load environment variables from the `.env` file when starting the containers.

### Database

#### Ports

All ports are configured in the file `docker-compose.yml`.

#### Passwords

All passwords have a default value in `docker-compose.yml`. (Keep in mind that you should change the values both here and in the script commands)

#### Volumes

The location of where the data is saved is also configurable in `docker-compose.yml`.

## Installation
    
This setup will raise 5 containers: one for each database, one for the Flask server, one for Kafka, and one for the Kafka producers & consumers.

```bash
docker compose up -d
```

## Scripts

To populate the databases with dummy data for testing, you can run the following commands. This setup ensures both the relational (MySQL) and graph (Neo4j) databases are initialized with appropriate dummy data.

### MySQL
```bash
sudo docker exec -i mysql mysql -u root -prootpassword < scripts/mysql/create_database.sql
```

```bash
sudo docker exec -i mysql mysql -u root -prootpassword < scripts/mysql/clothes.sql
```

### Neo4j

```bash
python3 scripts/neo4j/generate_neo4j_data.py
```

```bash
sudo docker exec -i neo4j cypher-shell -u neo4j -p password < neo4j_data.cypher
```

## Authors

- [@EliteOneTube](https://github.com/EliteOneTube)