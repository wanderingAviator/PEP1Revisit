from flask import json
from my_mongo_connection import order, product
from datetime import datetime
from bson import json_util, ObjectId

def parse_json(data):
    return json.loads(json_util.dumps(data))

#create order
def create_order(order_object):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    total_price = 0
    items = order_object['products']
    print("Order: ", order_object)
    print('Products: ', items)
    for item in items:
        product_doc = product.find_one({"_id": ObjectId(item["product_id"])})
        if product_doc:
            total_price += product_doc["product_price"] * item["quantity"]

    return order.insert_one({
        "customer_id" : order_object["customer_id"],
        "products" : items,
        "total_price" : total_price,
        "order_date" : now,
    })

#update order/ More of admin use case
def update_order(id, order_object):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    filter = {"_id" : id}
    update = {"$set": {
        "customer_id" : order_object["customer_id"],
        "products" : order_object['products'],
        "total_price" : order_object['total_price'],
        "updated_at" : now
    }}
    order.update_one(filter, update)

#find by id
def find_by_id(id):
    return parse_json(order.find_one({"_id" : id}))

#get all
def get_all_orders():
    return parse_json(order.find({}))

# get orders by customer id
def get_by_customer(customer_id):
    return parse_json(order.find({"customer_id": customer_id}))

def get_orders_sorted_by_date(customer_id):
    pipeline = [{"$match": {"customer_id": customer_id}},
                {"$sort": {"order_date": -1}}]
    return parse_json(order.aggregate(pipeline))

#delete / More of an admin functionality
def delete_order(id):
    order.delete_one({"_id" : id})