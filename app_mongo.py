from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse
import product_api, user_api, review_api, order_api
from bson import ObjectId

app = Flask(__name__)
api = Api(app)

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

review_post_args = reqparse.RequestParser()
review_post_args.add_argument("customer_id", type=str, help="Customer id is required", required=True)
review_post_args.add_argument("product_id", type=str, help="Product id is required", required=True)
review_post_args.add_argument("rating", type=float, help="In Stock is required", required=True)
review_post_args.add_argument("comment", type=str, help="Comment is required", required=True)

review_update_args = reqparse.RequestParser()
review_update_args.add_argument("customer_id", type=str)
review_update_args.add_argument("product_id", type=str)
review_update_args.add_argument("rating", type=float)
review_update_args.add_argument("comment", type=str)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("first_name", type = str, help="First name is required", required=True)
user_post_args.add_argument("last_name", type = str, help="Last name is required", required=True)
user_post_args.add_argument("username", type = str, help="Username is required", required=True)
user_post_args.add_argument("address", type = str, help="Address is required", required=True)
user_post_args.add_argument("email", type = str, help="E-mail is required", required=True)
user_post_args.add_argument("password", type = str, help="Password is required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("first_name", type = str)
user_update_args.add_argument("last_name", type = str)
user_update_args.add_argument("username", type = str)
user_update_args.add_argument("address", type = str)
user_update_args.add_argument("email", type = str)
user_update_args.add_argument("password")

order_post_args = reqparse.RequestParser()
order_post_args.add_argument("customer_id", type=str, help="Customer id is required", required=True)
order_post_args.add_argument("products", type=list, help="Product ID list is required", required=True) #a list of product IDs

order_update_args = reqparse.RequestParser()
order_update_args.add_argument("customer_id", type=str)
order_update_args.add_argument("products", type='list')
order_update_args.add_argument("total_price", type=float)

# Classes

#PRODUCT
class Product(Resource): #all require an ID to operate on
    def get(self, id):
        object_id = ObjectId(id)
        return product_api.find_by_id(object_id)
    
    def put(self, id):
        object_id = ObjectId(id)
        args = product_update_args.parse_args()
        product_api.update_product(object_id, args)

    def delete(self, id):
        object_id = ObjectId(id)
        product_api.delete_product(object_id)

class ReturnAllProducts(Resource): #Don't require anything to operate on
    def get(self):
        return product_api.get_all_products()
    
    def post(self):
        args = product_post_args.parse_args()
        product_api.create_product(args)

#USER
class UserByID(Resource):  #all require an ID to operate on
    def get(self, id):
        object_id = ObjectId(id)
        return user_api.find_by_id(object_id)  
    
    def put(self, id):
        object_id = ObjectId(id)
        args = user_update_args.parse_args()
        user_api.update_user_by_id(object_id, args)

    def delete(self, id):
        object_id = ObjectId(id)
        user_api.delete_user_by_id(object_id)

class UserByUsername(Resource):  #all require a username to operate on
    def get(self, username):
        return user_api.find_by_username(username)  
    
    def put(self, username):
        args = user_update_args.parse_args()
        user_api.update_user_by_username(username, args)

    def delete(self, username):
        user_api.delete_user_by_username(username)

class ReturnAllUsers(Resource): #Don't require anything to operate on
    def get(self):
            return user_api.find_all()
    
    def post(self):
         args = user_post_args.parse_args()
         user_api.create_user(args) 

class UserByFullName(Resource): #some searches by name, for fun
    def get(self, name):
         return user_api.find_by_full_name(name)
    
class UserByFirstName(Resource):
    def get(self, fname):
         return user_api.find_by_first_name(fname)
    
class UserByLastName(Resource):
    def get(self, lname):
         return user_api.find_by_last_name(lname)

# REVIEW
class ReviewByID(Resource): #all require an ID to operate on
    def get(self, review_id):
        object_id = ObjectId(review_id)# Convert the string item_id to ObjectId
        review = review_api.find_by_id(object_id)
        if review:
            return review, 200
        else:
            return {"message": "Review not found"}, 404

    def put(self, review_id):
        args = review_post_args.parse_args()
        object_id = ObjectId(review_id)# Convert the string item_id to ObjectId

        result = review_api.update_review(object_id, args)
        if result.modified_count > 0:
            return {"message": "Review updated successfully"}, 200
        else:
            return {"message": "Review not found"}, 404
    
    def delete(self, review_id):
        # Convert the string item_id to ObjectId
        object_id = ObjectId(review_id)
        result = review_api.delete_review(object_id)
        if result.deleted_count > 0:
            return {"message": "Review deleted successfully"}, 200
        else:
            return {"message": "Review not found"}, 404
        
class ReturnAllReviews(Resource): #Don't require anything to operate on
    def get(self):
            return review_api.find_all(), 200
    
    def post(self):
        args = review_post_args.parse_args()
        result = review_api.create_review(args)
        return {"message": "Review created", "inserted_id": str(result.inserted_id)}, 201
    

class ReviewByCustomer(Resource): #some extra searches, for fun
    def get(self, customer_id):
        return review_api.find_by_customer(customer_id), 200
    
class ReviewByProduct(Resource): #some extra searches, for fun
    def get(self, product_id):
        return review_api.find_by_product(product_id), 200

#ORDER
class OrderByID(Resource): #Require ID
    def get(self, order_id):
        object_id = ObjectId(order_id)
        return order_api.find_by_id(object_id)  
    
    def put(self, order_id):
        object_id = ObjectId(order_id)
        args = order_update_args.parse_args()
        order_api.update_order(object_id, args)

    def delete(self, id):
        object_id = ObjectId(id)
        order_api.delete_order(object_id)

class ReturnAllOrders(Resource): #don't require id
    def get(self):
        return order_api.get_all_orders()
    
    def post(self):
         args = order_post_args.parse_args()
         order_api.create_order(args) 

class OrderByCustomer(Resource): #extra search for fun
    def get(self, customer_id):
        return order_api.get_by_customer(customer_id)
    
class OrderByCustomerAndDate(Resource): #extra search for fun, plus a means to sort by date
    def get(self, customer_id):
        return order_api.get_orders_sorted_by_date(customer_id)

   
api.add_resource(Product, '/product/<id>')
api.add_resource(ReturnAllProducts, '/product')

api.add_resource(UserByID, '/user/id/<id>')
api.add_resource(UserByUsername, '/user/username/<username>')
api.add_resource(ReturnAllUsers, '/user')
api.add_resource(UserByFullName, '/user/<name>')
api.add_resource(UserByFirstName, '/user/f/<fname>')
api.add_resource(UserByLastName, '/user/l/<lname>')

api.add_resource(ReturnAllReviews, '/review')
api.add_resource(ReviewByID, '/review/id/<string:review_id>')
api.add_resource(ReviewByCustomer, '/review/customer/<customer_id>')
api.add_resource(ReviewByProduct, '/review/product/<product_id>')

api.add_resource(ReturnAllOrders, '/order')
api.add_resource(OrderByID, '/order/id/<order_id>')
api.add_resource(OrderByCustomer, '/review/customer/<string:customer_id>')
api.add_resource(OrderByCustomerAndDate, '/review/customer/<string:customer_id>/bydate')

if __name__ == "__main__":
    app.run(debug=True)