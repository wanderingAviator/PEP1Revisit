from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
import product_api, user_api, review_api

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


#for review
review_post_args = reqparse.RequestParser()
review_post_args.add_argument("customer_id", type=int, help="Name is required", required=True)
review_post_args.add_argument("product_id", type=int, help="Description is required", required=True)
review_post_args.add_argument("rating", type=float, help="In Stock is required", required=True)
review_post_args.add_argument("comment", type=str, help="Comment is required", required=True)

review_update_args = reqparse.RequestParser()
review_update_args.add_argument("customer_id", type=int)
review_update_args.add_argument("product_id", type=int)
review_update_args.add_argument("rating", type=float)
review_update_args.add_argument("comment", type=str)

#endpoints
@app.route('/product', methods=['POST'])
def post_product(productObject):
    product_api.create_product(productObject)

@app.route('/review', methods=['POST'])
def post_review(review_object):
    review_api.create_review(review_object)

# Classes
class Product(Resource):
    def get(self, name):
        return product_api.find_by_name(name)
    
    def post(self, name):
        args = product_post_args.parse_args()
        product_api.create_product(args)
    
    def post(self, name):
        args = product_post_args.parse_args()
        product_api.create_product(args)


class Review(Resource):
    def get_all(self):
        return review_api.find_all()
    
    def get_by_product(self, product_id):
        return review_api.find_by_product(product_id)
    
    def get_by_customer(self, customer_id):
        return review_api.find_by_customer(customer_id)
    
    def post(self):
        args = review_post_args.parse_args()
        review_api.create_review(args)
    
    

print(product_api.find_by_name("Air Jordan")) 
api.add_resource(Product, '/product/<name>')
api.add_resource(Review, '/review/')

#USER

@app.route('/dashboard/customer')
def query_all_custs():
    return user_api.find_all()

@app.route('/dashboard/customer/<int:id>/')
def query_cust_by_number(id):
    return user_api.find_by_id(id)

#REVIEW


if __name__ == "__main__":
    app.run(debug=True)