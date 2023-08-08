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

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("first_name", type = str, help="First name is required", required=True)
user_post_args.add_argument("last_name", type = str, help="Last name is required", required=True)
user_post_args.add_argument("username", type = str, help="Username is required", required=True)
user_post_args.add_argument("address", type = str, help="Address is required", required=True)
user_post_args.add_argument("email", type = str, help="E-mail is required", required=True)
user_post_args.add_argument("hashed_password", type = str, help="Password is required", required=True)

#endpoints
@app.route('/product', methods=['POST'])
def post_product(productObject):
    product_api.create_product(productObject)

class Product(Resource):
    def get(self, name):
        return product_api.find_by_name(name)
    
    def put(self, name):
        args = product_update_args.parse_args()
        product_api.update_product(name, args)
    
    def post(self, name):
        args = product_post_args.parse_args()
        product_api.create_product(args)

    def delete(self, name):
        product_api.delete_product(name)

class User(Resource):
    def post(self, username):
         args = user_post_args.parse_args()
         user_api.create_user(args) 

    def get(self, username):
        return user_api.find_by_username(username)   



api.add_resource(Product, '/product/<name>')
api.add_resource(User, '/user/<username>')

#USER

@app.route('/dashboard/customer')
def query_all_custs():
    return user_api.find_all()

@app.route('/dashboard/customer/<int:id>/')
def query_cust_by_number(id):
    return user_api.find_by_id(id)



if __name__ == "__main__":
    app.run(debug=True)