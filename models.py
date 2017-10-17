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
            'dateCreated': str(datetime.now())
        }

        return file_data


       
class Folder(File):
    pass