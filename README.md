
# Extract Transform Load procedure

## Tech Stack

**Server:** Flask(python)

**Database:** MongoDB, Neo4j, Mysql

**Messaging**: Kafka


## Environment Variables

### Database

#### Ports

All ports are configured in the file `docker-compose.yml`.

#### Passwords

All passwords have a default value in `docker-compose.yml`. (Keep in mind that you should change the values both here and in the script commands)

#### Volumes

The location of where the data is saved is also configurable in `docker-compose.yml`.
## Installation
    
- Will raise 5 containers. One for each database, one for flask server and one for Kafka.
```bash
docker compose up -d
```
## Scripts

To populate the databases with dummy data for testing, you can run the following commands. This setup ensures both the relational (MySQL) and graph (Neo4j) databases are initialized with appropriate dummy data.

### Mysql
```bash
docker exec -i mysql mysql -u root -p rootpassword < scripts/mysql/create_database.sql
docker exec -i mysql mysql -u root -p rootpassword < scripts/mysql/clothes.sql
```

### Neo4j

```bash
python scripts/neo4j/generate_neo4j_data.py
```

```bash
docker exec -i neo4j cypher-shell -u neo4j -p password < scripts/neo4j/neo4j_data.cypher
```
## Authors

- [@EliteOneTube](https://github.com/EliteOneTube)

