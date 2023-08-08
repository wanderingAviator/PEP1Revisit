from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_restful import Resource, Api
import product_api, user_api

app = Flask(__name__)
api = Api(app)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#PRODUCT

@app.route('/product', methods=['POST'])
def post_product(productObject):
    product_api.create_product(productObject)

class Product(Resource):
    def get(self, name):
        return product_api.find_by_name(name)
    

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