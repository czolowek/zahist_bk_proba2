import os 
from typing import Optional

from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from dotenv import load_dotenv
from flask_migrate import Migrate
from src.database.base import db
from src.database import db_actions
from src.data import parse_rozetka
from src.database import db_actions


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URI')
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)



# with app.app_context():
#     db.create_all()




class ProductAPI(Resource):
    def get(self, product_id: Optional[str] = None):
        if product_id:
            product = db_actions.get_product(product_id)
            response = jsonify(product)
        else:
            products = db_actions.get_products()
            response = jsonify(products)

        response.status_code = 200
        return response
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("price")
        parser.add_argument("img_url")
        kwargs = parser.parse_args()
        msg = db_actions.add_product(**kwargs)
        response = jsonify(msg)
        response.status_code = 201
        return response
    
    def put(self, product_id: str):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("price")
        parser.add_argument("img_url")
        kwargs = parser.parse_args()
        msg = db_actions.update_product(product_id, **kwargs)
        response = jsonify(msg)
        response.status_code = 200
        return response
    
    def patch(self, product_id: str):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("name")
        kwargs = parser.parse_args()
        msg = db_actions.add_review_product(product_id, **kwargs)
        response = jsonify(msg)
        response.status_code = 200
        return response
    
class UserAPI(Resource):
    def post(self, product_id: str):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Поле 'name' обязательно.")
        kwargs = parser.parse_args()

        # Передаём аргумент 'name' в функцию buy_product
        msg = db_actions.buy_product(product_id, **kwargs)
        response = jsonify(msg)
        response.status_code = 201
        return response
    
api.add_resource(ProductAPI, "/api/products/", "/api/products/<product_id>/")
api.add_resource(UserAPI, "/api/users/<product_id>/")

if __name__ == "__main__":
    app.run(debug=True, port=3000)


