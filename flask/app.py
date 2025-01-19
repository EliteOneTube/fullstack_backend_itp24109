from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://mongodb:27017")  # Replace with your MongoDB URI
db = client["users_db"]
users_collection = db["users"]
products_collection = db["products"]

@app.route("/user/<user_id>/products", methods=["GET"])
def get_user_products(user_id):
    """Fetch products purchased by the user, their friends, and colleagues."""
    
    # Get user data from MongoDB
    user = users_collection.find_one({"userID": user_id})
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    purchased_products = []
    
    # Add the products purchased by the user
    user_products = products_collection.find({"user_id": user_id})
    for product in user_products:
        purchased_products.append(product)

    # Add the products purchased by the user's friends
    for friend_id in user.get("friends", []):
        friend_products = products_collection.find({"user_id": friend_id})
        for product in friend_products:
            purchased_products.append(product)

    # Add the products purchased by the user's colleagues
    for colleague_id in user.get("colleagues", []):
        colleague_products = products_collection.find({"user_id": colleague_id})
        for product in colleague_products:
            purchased_products.append(product)
    
    if not purchased_products:
        return jsonify({"message": "No products found for the user or their network"}), 404
    
    return dumps(purchased_products), 200

@app.route("/user/<user_id>/recommend", methods=["GET"])
def recommend_product(user_id):
    """Recommend a product that the user has not purchased, but their friends or colleagues have, 
    or recommend the most popular product if none are found."""
    
    # Get user data from MongoDB
    user = users_collection.find_one({"userID": user_id})
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Get the products purchased by the user's friends and colleagues
    recommended_products = []
    
    friends_and_colleagues = user.get("friends", []) + user.get("colleagues", [])
    
    purchased_product_ids = set(product["clothID"] for product in products_collection.find({"user_id": user_id}))
    
    for person_id in friends_and_colleagues:
        person_products = products_collection.find({"user_id": person_id})
        for product in person_products:
            if product["clothID"] not in purchased_product_ids:
                recommended_products.append(product)

    # If we found recommended products, return them
    if recommended_products:
        return dumps(recommended_products), 200  # Use bson.json_util.dumps to handle BSON serialization
    
    # If no recommended products were found, recommend the most popular product
    print("No products from friends or colleagues. Recommending the most popular product...")
    return popular_recommend_product(user_id)


def popular_recommend_product(user_id):
    """Recommend the most popular product that the user has not purchased."""
    
    # Get user data from MongoDB
    user = users_collection.find_one({"userID": user_id})
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Get the products purchased by the user's colleagues
    colleagues_products = set()
    for colleague_id in user.get("colleagues", []):
        colleague_products = products_collection.find({"userID": colleague_id})
        for product in colleague_products:
            colleagues_products.add(product["clothID"])
    
    # Get products already purchased by the user
    purchased_product_ids = set(product["clothID"] for product in products_collection.find({"userID": user_id}))
    
    # If the user has purchased all the products their colleagues have bought, suggest the most popular one
    if colleagues_products.issubset(purchased_product_ids):
        # Get the most popular product that the user has not purchased
        popular_product = products_collection.aggregate([
            {"$group": {"_id": "$clothID", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ])
        
        for product in popular_product:
            popular_product_id = product["_id"]
            if popular_product_id not in purchased_product_ids:
                # If the user hasn't purchased the popular product, return it
                recommended_product = products_collection.find_one({"clothID": popular_product_id})
                if recommended_product:
                    return jsonify(recommended_product), 200
    
    # If no popular product is found
    return jsonify({"message": "No recommendation available"}), 404

if __name__ == "__main__":
    app.run(debug=True)
