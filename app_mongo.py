from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_restful import Resource, Api
from product_api import create_product, find_by_name

app = Flask(__name__)
api = Api(app)

air_jordan = {
    "product_name" : "Air Jordan",
    "product_desc" : "Basketball Shoe",
    "in_stock" : True,
    "product_price" : "$100",
    "product_category" : "Shoes",
    "product_brand" : "Nike"
}

@app.route('/product', methods=['POST'])
def post_product(productObject):
    create_product(productObject)

#post_product(air_jordan)
#print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

class Product(Resource):
    def get(self, name):
        return find_by_name(name)
    

print(find_by_name("Air Jordan")) 
api.add_resource(Product, '/product/<name>')

if __name__ == "__main__":
    app.run(debug=True)