from ..mongo_connection.my_mongo_connection import review
from datetime import datetime

#create review
def create_review(reviewObject):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    review.insert_one({
        "customer_id" : reviewObject["customer_id"],
        "product_id" : reviewObject["product_id"],
        "rating" : reviewObject["rating"],
        "comment" : reviewObject["comment"],
        "updated_at" : now
    })

#update review
def update_review(id, reviewObject):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Defining the filter
    filter = {"_id": id}
    # defining what we want updated
    update = {"$set": {
        "customer_id" : reviewObject["customer_id"],
        "product_id" : reviewObject["product_id"],
        "rating" : reviewObject["rating"],
        "comment" : reviewObject["comment"],
        "updated_at" : now
    }}
    review.update_one(filter, update)

# find all
def find_all():
    return review.find({})

#find by product id
def find_by_product(product_id):
    return review.find({"product_id": product_id})

#find by customer id
def find_by_customer(customer_id):
    return review.find({"customer_id": customer_id})

#find by id
def find_by_id(id):
    return review.find_one({"_id": id})

#delete
def delete_review(id):
    review.delete_one({"_id":id})