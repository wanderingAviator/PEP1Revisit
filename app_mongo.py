import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
import product_api, user_api, review_api, order_api
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Allow all origins
app.config['JWT_SECRET_KEY'] = 'Barcelona'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)  
api = Api(app)
jwt = JWTManager(app)

#Request parsing set-up
product_post_args = reqparse.RequestParser()
product_post_args.add_argument("product_name", type=str, help="Name is required", required=True)
product_post_args.add_argument("product_desc", type=str, help="Description is required", required=True)
product_post_args.add_argument("in_stock", type=bool, help="In Stock is required", required=True)
product_post_args.add_argument("product_price", type=float, help="Price is required", required=True)
product_post_args.add_argument("product_category", type=str, help="Category is required", required=True)
product_post_args.add_argument("product_brand", type=str, help="Brand is required", required=True)

product_update_args = reqparse.RequestParser()
product_update_args.add_argument("product_name", type=str)
product_update_args.add_argument("product_desc", type=str)
product_update_args.add_argument("in_stock", type=bool)
product_update_args.add_argument("product_price", type=float)
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

user_authentication = reqparse.RequestParser()
user_authentication.add_argument("username", type=str, help="Username is required", required=True)
user_authentication.add_argument("password", type=str, help="Password is required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("first_name", type = str)
user_update_args.add_argument("last_name", type = str)
user_update_args.add_argument("username", type = str)
user_update_args.add_argument("address", type = str)
user_update_args.add_argument("email", type = str)
user_update_args.add_argument("password")

order_post_args = reqparse.RequestParser()
order_post_args.add_argument("customer_id", type=str, help="Customer id is required", required=True)
order_post_args.add_argument("products", type=list, location="json", help="Products list is required", required=True) #a list of product IDs

order_update_args = reqparse.RequestParser()
order_update_args.add_argument("products", type=list, location="json")

# Classes

#PRODUCT
class Product(Resource): #all require an ID to operate on
    def get(self, id):
        object_id = ObjectId(id)
        product = product_api.find_by_id(object_id)
        if product:
            return product, 200
        else:
            return {"message": "Product not found"}, 404
    
    def put(self, id):
        object_id = ObjectId(id)
        args = product_update_args.parse_args()
        result = product_api.update_product(object_id, args)
        if result.modified_count > 0:
            return {"message": "Product updated successfully"}, 200
        else:
            return {"message": "Product not found"}, 404

    def delete(self, id):
        object_id = ObjectId(id)
        result = product_api.delete_product(object_id)
        if result.deleted_count > 0:
            return {"message": "Product deleted successfully"}, 200
        else:
            return {"message": "Product not found"}, 404

class ReturnAllProducts(Resource): #Don't require anything to operate on
    def get(self):
        return product_api.get_all_products(), 200
    
    def post(self):
        args = product_post_args.parse_args()
        result = product_api.create_product(args)
        return {"message": "Product created", "inserted_id": str(result.inserted_id)}, 201

#USER
class UserAuthentication(Resource): # authenticating the user by username and password
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user:
            return current_user, 200
        return {"message": "Unauthorized"}, 401

    def post(self):
        args = user_authentication.parse_args()
        return user_api.authenticate_login(args)


class UserByID(Resource):  #all require an ID to operate on
    @jwt_required()
    def get(self, id):
        current_user = get_jwt_identity()
        if str(current_user["_id"]['$oid']) == id:
            object_id = ObjectId(id)
            user = user_api.find_by_id(object_id)  
            if user:
                return user, 200
            else:
                return {"message": "User not found"}, 404
        else:
            return {"message": "Unauthorized"}, 401
    
    def put(self, id):
        object_id = ObjectId(id)
        args = user_update_args.parse_args()
        result = user_api.update_user_by_id(object_id, args)
        if result.modified_count > 0:
            return {"message": "User updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    def delete(self, id):
        object_id = ObjectId(id)
        result = user_api.delete_user_by_id(object_id)
        if result.deleted_count > 0:
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

class UserByUsername(Resource):  #all require a username to operate on
    def get(self, username):
        user = user_api.find_by_username(username)  
        if user:
            return user, 200
        else:
            return {"message": "User with username '" + username + "' not found"}, 404
    
    def put(self, username):
        args = user_update_args.parse_args()
        result = user_api.update_user_by_username(username, args)
        if result.modified_count > 0:
            return {"message": "User with username '" + username + "' updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    def delete(self, username):
        result = user_api.delete_user_by_username(username)
        if result.deleted_count > 0:
            return {"message": "User with username '" + username + "' deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

class ReturnAllUsers(Resource): #Don't require anything to operate on
    def get(self):
            return user_api.find_all(), 200
    
    def post(self):
        args = user_post_args.parse_args()
        result = user_api.create_user(args) 
        return {"message": "User created", "inserted_id": str(result.inserted_id)}, 201

class UserByFullName(Resource): #some searches by name, for fun
    def get(self, name):
         return user_api.find_by_full_name(name), 200
    
class UserByFirstName(Resource):
    def get(self, fname):
         return user_api.find_by_first_name(fname), 200
    
class UserByLastName(Resource):
    def get(self, lname):
         return user_api.find_by_last_name(lname), 200

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
        order = order_api.find_by_id(object_id)  
        if order:
            return order, 200
        else:
            return {"message": "Order not found"}, 404

    
    def put(self, order_id):
        object_id = ObjectId(order_id)
        args = order_update_args.parse_args()
        result = order_api.update_order(object_id, args)
        if result.modified_count > 0:
            return {"message": "Order updated successfully"}, 200
        else:
            return {"message": "Order not found"}, 404

    def delete(self, order_id):
        object_id = ObjectId(order_id)
        result = order_api.delete_order(object_id)
        if result.deleted_count > 0:
            return {"message": "Order deleted successfully"}, 200
        else:
            return {"message": "Order not found"}, 404

class ReturnAllOrders(Resource): #don't require id
    def get(self):
        return order_api.get_all_orders(), 200
    
    def post(self):
        args = order_post_args.parse_args()
        result = order_api.create_order(args) 
        return {"message": "Order created", "inserted_id": str(result.inserted_id)}, 201

class OrderByCustomer(Resource): #extra search for fun
    def get(self, customer_id):
        return order_api.get_by_customer(customer_id), 200
    
class OrderByCustomerAndDate(Resource): #extra search for fun, plus a means to sort by date
    def get(self, customer_id):
        return order_api.get_orders_sorted_by_date(customer_id), 200

   
api.add_resource(Product, '/product/<string:id>')
api.add_resource(ReturnAllProducts, '/product')

api.add_resource(UserAuthentication, '/login', '/profile')
api.add_resource(UserByID, '/user/id/<string:id>')
api.add_resource(UserByUsername, '/user/username/<username>')
api.add_resource(ReturnAllUsers, '/user')
api.add_resource(UserByFullName, '/user/<name>')
api.add_resource(UserByFirstName, '/user/f/<fname>')
api.add_resource(UserByLastName, '/user/l/<lname>')

api.add_resource(ReturnAllReviews, '/review')
api.add_resource(ReviewByID, '/review/id/<string:review_id>')
api.add_resource(ReviewByCustomer, '/review/customer/<string:customer_id>')
api.add_resource(ReviewByProduct, '/review/product/<string:product_id>')

api.add_resource(ReturnAllOrders, '/order')
api.add_resource(OrderByID, '/order/id/<string:order_id>')
api.add_resource(OrderByCustomer, '/order/customer/<string:customer_id>')
api.add_resource(OrderByCustomerAndDate, '/order/customer/<string:customer_id>/bydate')

if __name__ == "__main__":
    app.run(debug=True)