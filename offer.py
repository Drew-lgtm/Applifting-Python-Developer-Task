import sqlite3
from flask_restful import Resource, reqparse


class Offer():
    TABLE_NAME = 'offers'

    def __init__(self, _id, price, items_in_stock):
        self.id = _id
        self.price = price
        self.items_in_stock = items_in_stock

    @classmethod
    # classmethod >> cls instead of self
    def find_by_price(cls, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE price=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (price,))
        row = result.fetchone()
        if row is not None:
            offer = cls(*row)
        else:
            offer = None

        connection.close()
        return offer

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            offer = cls(*row)
        else:
            offer = None

        connection.close()
        return offer


class PlaceOffer(Resource):
    TABLE_NAME = 'offers'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('items_in_stock',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )



    def post(self):
        data = PlaceOffer.parser.parse_args()


        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['price'], data['items_in_stock']))

        connection.commit()
        connection.close()

        return {"message": "Offer created successfully."}, 201
