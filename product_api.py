from flask import json
from my_mongo_connection import product
from datetime import datetime
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

#create product
def create_product(productObject):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    product.insert_one({
        "product_name" : productObject['product_name'],
        "product_desc" : productObject['product_desc'],
        "in_stock" : productObject['in_stock'],
        "product_price" : productObject['product_price'],
        "product_category" : productObject['product_category'],
        "product_brand" : productObject['product_brand'],
        "updated_at" : now
    })

#update product
def update_product(id, productObject):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    product.update_one({
        {"_id" : id},{
        "product_name" : productObject.name,
        "product_desc" : productObject.desc,
        "in_stock" : productObject.in_stock,
        "product_price" : productObject.price,
        "product_category" : productObject.category,
        "product_brand" : productObject.brand,
        "updated_at" : now
        }
    })

#find by id 
def find_by_id(id):
    return product.find_one({"_id" : id})

#find by name
def find_by_name(name):
    return parse_json(product.find_one({"product_name" : name}))

#get all
def get_all_products():
    return product.find({})

#delete
def delete_product(id):
    product.delete_one({"_id" : id})
