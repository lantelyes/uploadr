from flask import request, Response, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_restful import Resource, Api
from datetime import datetime
import os, json
import textract



client = MongoClient()
db = client.file_database
file_collection = db.file_collection


UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['pdf','doc','docx'])

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class Upload(Resource):

    def post(self):

        size = 0
        path = ""

        file = request.files['file']
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
        else:
            return Response(status=400, mimetype='application/json')

        
        ext = filename.rsplit('.', 1)[1].lower()
        name = filename.rsplit('.', 1)[0]
        size = size = os.stat(path).st_size
        text = textract.process(path)


        file_data = {
            'name': name,
            'size_in_Kb': size,
            'date_created': str(datetime.now()),
            'path': path,
            'description': None,
            'extention': ext,
            'text': text
        }

        file_collection.insert_one(file_data)

        return Response(status=200, mimetype='application/json')

class File(Resource):

    def get(self):
        filename = request.args.get("name")
        if filename:
            return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
        else:
            return Response(status=400, mimetype='application/json')
    

    def post(self):
        file = json.loads(request.data)


        oid = ObjectId(file['_id'])
        description = file['description']

        file_collection.update_one({'_id' : oid},{"$set": {"description" : description}}, False)

        return Response(status=200, mimetype='application/json')

def serialize_file_list(file_list):
        for f in file_list:
            f['_id'] = str(f['_id'])
            f['date_created'] = str(f['date_created'])

        return file_list
       
def build_search_qeuery(query, types, extentions):

    query_object = {}

    name_query = {}
    ext_query = {}
    contents_query = {}

    if extentions:
        ext_query = {"$or" : []}
        for ext in extentions:
            ext_query["$or"].append({"extention": ext})
    
    if "name" in types:
        name_query = {"name":  {'$regex': query, "$options" : "i"} }
    if "contents" in types:
        contents_query = {"text":  {'$regex': query, "$options" : "i"} }

    query_object =  {"$and": [name_query, contents_query, ext_query]}

    print query_object

    return query_object



class List(Resource):
    def get(self):

        search_query = request.args.get("query")
        serach_types = request.args.getlist("type")
        search_extentions = request.args.getlist("ext")

        query_object = build_search_qeuery(search_query, serach_types, search_extentions)


    
        file_list = list(file_collection.find(query_object))
    

        return  serialize_file_list(file_list)
        
