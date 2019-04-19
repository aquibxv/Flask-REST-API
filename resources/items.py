import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This feild cannot be left blank"
    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
           return item.json()
        return {'message' : 'Item not found'}, 404

    def post(self, name):
        # if an item with the name already exists
        if ItemModel.find_by_name(name):
            return {"message" : "Item with name already exists"}

        data = Item.parser.parse_args()
        # else create the object
        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {'message' : 'An Error occured while inserting an item'}, 500 # Internal Server Error

        return item.json(), 201 

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
        
        return {'message' : 'Item has been deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

        
    