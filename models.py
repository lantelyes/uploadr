from flask import request
from pymongo import MongoClient
from flask_restful import Resource, Api
from datetime import datetime

client = MongoClient()
db = client.file_database
file_collection = db.file_collection

class File(Resource):

    def get(self):
        return "Hello, world"

    def post(self):
        size = request.args.get('size_in_kb')
        name = request.args.get('name')
        uri = request.args.get('uri')


        file_data = {
            'name': name,
            'size_in_Kb': size,
            'is_folder': False,
            'uri': uri,
            'date_created': str(datetime.now())
        }

        file_collection.insert_one(file_data)
        file_data['_id'] = str(file_data['_id'])

        return file_data


       
class List(Resource):
    def get(self):

        file_list = list(file_collection.find())

        for f in file_list:
            f['_id'] = str(f['_id'])
            f['date_created'] = str(f['date_created'])

        return  file_list
        
