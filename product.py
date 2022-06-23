from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
import sqlite3


class Product(Resource):
    TABLE_NAME = 'products'

    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # @jwt_required()
    def get(self, name):
        product = self.find_by_name(name)
        if product is not None:
            return product
        return {'message': 'Product not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'product': {'name': row[0], 'description': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An product with name '{}' already exists.".format(name)}

        data = Product.parser.parse_args()

        product = {'name': name, 'description': data['description']}

        try:
            Product.insert(product)
        except:
            return {"message": "An error occurred inserting the product."}

        return product, 201

    @classmethod
    def insert(cls, product):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (product['name'], product['description']))

        connection.commit()
        connection.close()

    # @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Product deleted'}

    # @jwt_required()
    def put(self, name):
        data = Product.parser.parse_args()
        product = self.find_by_name(name)
        updated_product = {'name': name, 'description': data['description']}
        if product is None:
            try:
                Product.insert(updated_product)
            except:
                return {"message": "An error occurred inserting the product."}
        else:
            try:
                Product.update(updated_product)
            except:
                return {"message": "An error occurred updating the product."}
        return updated_product

    @classmethod
    def update(cls, product):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET description=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (product['description'], product['name']))

        connection.commit()
        connection.close()


class ProductList(Resource):
    TABLE_NAME = 'products'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        products = []
        for row in result:
            products.append({'name': row[0], 'description': row[1]})
        connection.close()

        return {'products': products}
