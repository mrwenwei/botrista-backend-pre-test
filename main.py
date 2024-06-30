from flask import Flask
from flask_restful import Api
from config import Config
from database import db
from resources.signup import SignupResource
from resources.login import LoginResource
from resources.logout import LogoutResource
from resources.product import ProductResource
from resources.products import ProductsResource
from resources.order import OrderResource
from resources.orders import OrdersResource
from apidocs import init_swagger

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
api = Api(app)
init_swagger(app)

with app.app_context():
    db.create_all()

api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(ProductResource, '/product')
api.add_resource(ProductsResource, '/products')
api.add_resource(OrderResource, '/order')
api.add_resource(OrdersResource, '/orders')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
