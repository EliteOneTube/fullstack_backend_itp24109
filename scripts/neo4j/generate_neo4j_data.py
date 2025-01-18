import random

def generate_neo4j_data(num_users=100, max_purchased=1000, filename="./neo4j_data.cypher"):
    with open(filename, "w") as f:
        # Create users with random purchases
        for user_id in range(1, num_users + 1):
            name = f"User{user_id}"
            purchased = random.sample(range(1, max_purchased + 1), random.randint(1, 10))  # 1-10 purchases
            f.write(f'CREATE (u{user_id}:User {{userID: {user_id}, name: "{name}", purchased: {purchased}}});\n')

        # Create random relationships
        relationships = ["FRIENDS", "COLLEAGUES"]
        for user_id in range(1, num_users + 1):
            for _ in range(random.randint(1, 3)):  # Each user has 1-3 relationships
                target_id = random.randint(1, num_users)
                while target_id == user_id:  # Avoid self-relations
                    target_id = random.randint(1, num_users)
                relationship = random.choice(relationships)
                f.write(f'CREATE (u{user_id})-[:{relationship}]->(u{target_id});\n')

    print(f"Cypher script generated: {filename}")

# Generate a Cypher script with 100 users and up to 1000 purchased IDs
generate_neo4j_data(num_users=100, max_purchased=1000)