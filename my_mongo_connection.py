import pymongo

MONGO_URL = "mongodb://localhost:27017"

client = pymongo.MongoClient(MONGO_URL)

product_retail = client["ProductRetail"]

product = product_retail["Product"]
review = product_retail["Review"]
user = product_retail["User"]
order = product_retail["Order"]

# creating index for username 
user.create_index([("username", pymongo.ASCENDING)], unique=True)

# client.close()