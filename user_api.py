from my_mongo_connection import user
from datetime import datetime
from flask import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

#create user
def create_user(userObject):
    user.insert_one({
        "first_name" : userObject["first_name"],
        "last_name" : userObject["last_name"],
        "username" : userObject["username"],
        "email" : userObject["email"],
        "address" : userObject["address"],
        "hashed_password" : userObject["hashed_password"]
    })


#update review
def update_user(id, userObject):
    # Defining the filter
    filter = {"_id": id}
    # defining what we want updated
    update = {"$set": {
        "first_name" : userObject["first_name"],
        "last_name" : userObject["last_name"],
        "username" : userObject["username"],
        "email" : userObject["email"],
        "address" : userObject["address"],
        "hashed_password" : userObject["hashed_password"]
    }}
    user.update_one(filter, update)

# find all
def find_all():
    return user.find({})

def find_by_username(username):
    return parse_json(user.find({"username": username}))

def find_by_name(name):
    first_name, last_name = name.split()
    return parse_json(user.find({"first_name": first_name,
                      "last_name": last_name}))

#find by id
def find_by_id(id):
    return user.find_one({"_id":id})

#delete
def delete_user(id):
    user.delete_one({"_id":id})