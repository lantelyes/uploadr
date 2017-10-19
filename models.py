from flask import request, Response, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
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

            if not os.path.isfile(path):
                file.save(path)
            else:
                raise BadRequest("File already exists on server")
        else:
            raise BadRequest("File not one of the allowed types")

        
        ext = filename.rsplit('.', 1)[1].lower()
        name = filename.rsplit('.', 1)[0]
        size = size = os.stat(path).st_size
        text = textract.process(path)
        date_created = str(datetime.now()).split(" ")[0]


        file_data = {
            'name': name,
            'size_in_Kb': size,
            'date_created': date_created,
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
            raise BadRequest("No filename specified")
    

    def post(self):
        file = json.loads(request.data)

        oid = ObjectId(file['_id'])
        description = file['description']

        file_collection.update_one({'_id' : oid},{"$set": {"description" : description}}, False)

        return Response(status=200, mimetype='application/json')

    def delete(self):
        oid = request.args.get("oid")
        if oid:
            file = file_collection.find_one({"_id": ObjectId(oid)})
            if file:
                path = file["path"]
                if os.path.isfile(path):
                    os.remove(path)
                    file_collection.delete_one(file)
                else:
                    raise BadRequest("File not found in server storage") 
            else:
                raise BadRequest("File not found in database")
        else:
            raise BadRequest("No ObjectId provided for deletion")


        return Response(status=200, mimetype='application/json')
                
            
            

        

def serialize_file_list(file_list):
        for f in file_list:
            f['_id'] = str(f['_id'])
            f['date_created'] = str(f['date_created'])

        return file_list
       
def build_search_qeuery(query, types, extentions,case_sensitive):

    query_object = {}

    name_query = {}
    ext_query = {}
    contents_query = {}
    regex_options = "i"

    if case_sensitive:
        regex_options = ""

    if extentions:
        ext_query = {"$or" : []}
        for ext in extentions:
            ext_query["$or"].append({"extention": ext})
    
    if "name" in types:
        name_query = {"name":  {'$regex': query, "$options" : regex_options} }
    if "contents" in types:
        contents_query = {"text":  {'$regex': query, "$options" : regex_options} }

    query_object =  {"$and": [name_query, contents_query, ext_query]}

    print query_object

    return query_object



class List(Resource):
    def get(self):

        search_query = request.args.get("query")
        serach_types = request.args.getlist("type")
        search_extentions = request.args.getlist("ext")
        search_case_sensitive = request.args.getlist("case")

        query_object = build_search_qeuery(search_query, serach_types, search_extentions, search_case_sensitive)
        file_list = list(file_collection.find(query_object))
    

        return  serialize_file_list(file_list)
        
