from flask import json
from my_mongo_connection import review
from datetime import datetime
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

#create review
def create_review(reviewObject):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return review.insert_one({
        "customer_id" : reviewObject["customer_id"],
        "product_id" : reviewObject["product_id"],
        "rating" : reviewObject["rating"],
        "comment" : reviewObject["comment"],
        "created_at" : now,
        "updated_at": now
    })

#update review
def update_review(id, reviewObject):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Defining the filter
    filter = {"_id": id}
    # defining what we want updated
    update = {"$set": {
        "rating" : reviewObject["rating"],
        "comment" : reviewObject["comment"],
        "updated_at" : now
    }}
    return review.update_one(filter, update)

# find all
def find_all():
    return parse_json(review.find({}))

#find by product id
def find_by_product(product_id):
    return parse_json(review.find({"product_id": product_id}))

#find by customer id
def find_by_customer(customer_id):
    return parse_json(review.find({"customer_id": customer_id}))

#find by id
def find_by_id(id):
    return parse_json(review.find_one({"_id": id}))

# sort by rating
def sort_by_popularity():
    pipeline = [
        {
            '$sort': {'rating': -1 }
        }
    ]
    return parse_json(review.aggregate(pipeline))

# sort by popularity with the product id
def sort_by_popularity_with_product(product_id):
    pipeline = [
        {
            '$match': {'product_id': product_id}
        }, 
        {
            '$sort': {'rating': -1 }
        }
    ]
    return parse_json(review.aggregate(pipeline))

#calculate the average rating for a specific product
def calculate_avg_rating(product_id):
    pipeline = [
        {
            '$match': {'product_id': product_id}
        },
        {
            '$group': {'_id': '$product_id', 'average_rating': {'$avg': '$rating'}}
        }
    ]

    return parse_json(review.aggregate(pipeline))

#delete
def delete_review(id):
    return review.delete_one({"_id":id})