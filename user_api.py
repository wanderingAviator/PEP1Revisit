from my_mongo_connection import user
from datetime import datetime
from flask import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

#create user
def create_user(userObject):
    return user.insert_one({
        "first_name" : userObject["first_name"],
        "last_name" : userObject["last_name"],
        "username" : userObject["username"],
        "email" : userObject["email"],
        "address" : userObject["address"],
        "password" : userObject["password"]
    })

#update user
def update_user_by_id(id, userObject):
    # Defining the filter
    filter = {"_id": id}
    # defining what we want updated
    update = {"$set": {
        "first_name" : userObject["first_name"],
        "last_name" : userObject["last_name"],
        "username" : userObject["username"],
        "email" : userObject["email"],
        "address" : userObject["address"],
        "password" : userObject["password"]
    }}
    return user.update_one(filter, update)

def update_user_by_username(username, userObject):
    # Defining the filter
    filter = {"username": username}
    # defining what we want updated
    update = {"$set": {
        "first_name" : userObject["first_name"],
        "last_name" : userObject["last_name"],
        "username" : userObject["username"],
        "email" : userObject["email"],
        "address" : userObject["address"],
        "password" : userObject["password"]
    }}
    return user.update_one(filter, update)

# find
def find_all():
    return parse_json(user.find({}))

def find_by_username(username):
    return parse_json(user.find({"username": username}))

def find_by_full_name(name):
    first_name, last_name = name.split()
    return parse_json(user.find({"first_name": first_name,
                      "last_name": last_name}))

def find_by_first_name(name):
    return parse_json(user.find({"first_name": name}))

def find_by_last_name(name):
    return parse_json(user.find({"last_name": name}))

def find_by_id(id):
    return parse_json(user.find_one({"_id":id}))

#delete
def delete_user_by_id(id):
    return user.delete_one({"_id":id})

def delete_user_by_username(username):
    return user.delete_one({"username": username})