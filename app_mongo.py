from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
import product_api, user_api

app = Flask(__name__)
api = Api(app)

# MAIN PAGES
@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#PRODUCT

#Request parsing set-up
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

#endpoints
@app.route('/product', methods=['POST'])
def post_product(productObject):
    product_api.create_product(productObject)

class Product(Resource):
    def get(self, name):
        return product_api.find_by_name(name)
    
    def post(self, name):
        args = product_post_args.parse_args()
        product_api.create_product(args)
    
    def post(self, name):
        args = product_post_args.parse_args()
        product_api.create_product(args)
    

print(product_api.find_by_name("Air Jordan")) 
api.add_resource(Product, '/product/<name>')

#USER

@app.route('/dashboard/customer')
def query_all_custs():
    return user_api.find_all()

@app.route('/dashboard/customer/<int:id>/')
def query_cust_by_number(id):
    return user_api.find_by_id(id)

if __name__ == "__main__":
    app.run(debug=True)