from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT

# from security import authenticate, identity
from offer import PlaceOffer
from product import Product, ProductList

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

# jwt = JWT(app, authenticate, identity)

api.add_resource(Product, '/products/register/<string:name>')
api.add_resource(ProductList, '/products')
api.add_resource(PlaceOffer, '/offer')

# default address is http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)
