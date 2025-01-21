from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import logging

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://mongodb:27017")  # Replace with your MongoDB URI
db = client["fusion_db"]
users_collection = db["users"]
clothes_collection = db["clothes"]

@app.route("/user/<int:user_id>/products/", methods=["GET"])
@app.route("/user/<int:user_id>/products", methods=["GET"])
def get_user_products(user_id):
    """Fetch products purchased by the user, their friends, and colleagues."""
    
    # Step 1: Get the user's profile from the database
    user = users_collection.find_one({"userID": user_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    purchased_products = []

    # Step 2: Add the user's own purchased items
    user_purchased_ids = user.get("purchased", [])
    user_products = clothes_collection.find({"clothID": {"$in": user_purchased_ids}})
    purchased_products.extend(user_products)

    # Step 3: Fetch profiles of friends and colleagues
    related_user_ids = [rel["related_userID"] for rel in user.get("relationships", [])]
    related_users = users_collection.find({"userID": {"$in": related_user_ids}})

    # Step 4: Fetch products purchased by friends and colleagues
    related_purchased_ids = []
    for related_user in related_users:
        related_purchased_ids.extend(related_user.get("purchased", []))

    if related_purchased_ids:
        related_products = clothes_collection.find({"clothID": {"$in": related_purchased_ids}})
        purchased_products.extend(related_products)

    # If no products found, return a message
    if not purchased_products:
        return jsonify({"message": "No products found for the user or their network"}), 404

    # Step 5: Serialize and return the data
    return dumps(purchased_products), 200

@app.route("/user/<int:user_id>/recommend/", methods=["GET"])
@app.route("/user/<int:user_id>/recommend", methods=["GET"])
def recommend_product(user_id):
    """Recommend a product that the user has not purchased, but their friends or colleagues have,
    or recommend the most popular product if none are found."""
    user = users_collection.find_one({"userID": user_id})

    if not user:
        return jsonify({"error": "User not found"}), 404

    purchased_product_ids = {product["clothID"] for product in clothes_collection.find({"user_id": user_id})}
    recommended_products = []

    # Check friends' and colleagues' purchases
    for relationship in user.get("relationships", []):
        related_user_id = relationship["related_userID"]
        related_user_products = clothes_collection.find({"user_id": related_user_id})
        for product in related_user_products:
            if product["clothID"] not in purchased_product_ids:
                recommended_products.append(product)

    if recommended_products:
        return dumps(recommended_products), 200

    # If no recommendations found, suggest the most popular product
    return popular_recommend_product(user_id)


def popular_recommend_product(user_id):
    """Recommend the most popular product that the user has not purchased."""
    user = users_collection.find_one({"userID": user_id})

    if not user:
        return jsonify({"error": "User not found"}), 404

    purchased_product_ids = {product["clothID"] for product in clothes_collection.find({"user_id": user_id})}

    # Find the most popular product globally
    popular_product = [
        {"clothID": 1001, "count": 10},  # Mocking aggregated results
        {"clothID": 1002, "count": 8},
    ]

    for product in popular_product:
        if product["clothID"] not in purchased_product_ids:
            recommended_product = clothes_collection.find({"clothID": product["clothID"]})
            if recommended_product:
                return dumps(recommended_product), 200

    return jsonify({"message": "No recommendation available"}), 404

if __name__ == "__main__":
    app.run(debug=True)
