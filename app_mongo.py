from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
from product_api import create_product, find_by_name

app = Flask(__name__)
api = Api(app)

product_post_args = reqparse.RequestParser()
product_post_args.add_argument("product_name", type=str, help="Name is required", required=True)
product_post_args.add_argument("product_desc", type=str, help="Description is required", required=True)
product_post_args.add_argument("in_stock", type=bool, help="In Stock is required", required=True)
product_post_args.add_argument("product_price", type=str, help="Price is required", required=True)
product_post_args.add_argument("product_category", type=str, help="Category is required", required=True)
product_post_args.add_argument("product_brand", type=str, help="Brand is required", required=True)

product_update_args = reqparse.RequestParser()
product_update_args.add_argument("product_name", type=str)
product_update_args.add_argument("product_desc", type=str)
product_update_args.add_argument("in_stock", type=bool)
product_update_args.add_argument("product_price", type=str)
product_update_args.add_argument("product_category", type=str)
product_update_args.add_argument("product_brand", type=str)

air_jordan = {
    "product_name" : "Air Jordan",
    "product_desc" : "Basketball Shoe",
    "in_stock" : True,
    "product_price" : "$100",
    "product_category" : "Shoes",
    "product_brand" : "Nike"
}


class Product(Resource):
    def get(self, name):
        return find_by_name(name)
    
    def post(self, name):
        args = product_post_args.parse_args()
        create_product(args)
    

print(find_by_name("Air Jordan")) 
api.add_resource(Product, '/product/<name>')

if __name__ == "__main__":
    app.run(debug=True)