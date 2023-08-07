from ..mongo_connection.my_mongo_connection import product
from datetime import datetime

#create product
def create_product(productObject):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    product.insert_one({
        "product_name" : productObject.name,
        "product_desc" : productObject.desc,
        "in_stock" : productObject.in_stock,
        "product_price" : productObject.price,
        "product_category" : productObject.category,
        "product_brand" : productObject.brand,
        "updated_at" : now
    })
#update product

#find by id

