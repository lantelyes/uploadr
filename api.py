from flask import request, Response, send_from_directory
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest
from datetime import datetime
import os, json, textract
from utils import *
from constants import *


file_collection = init_database("file_collection")

#Upload endpoint
#Responsible for: uploading files from the frontend and saving them to the server filesystem and database 
class Upload(Resource):
    @auth.login_required
    def post(self):

        file = request.files['file']
        size = 0
        path = ""

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
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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

#File endpoint:
#Responsible for: Downloading, updating, and deleting files stored in the database and on the server
class File(Resource):
    @auth.login_required
    def get(self):

        filename = request.args.get("name")
        if filename:
            path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(path):
                return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
            else:
                raise BadRequest("File requested does not exist on server")
        else:
            raise BadRequest("No filename specified")
    
    @auth.login_required
    def post(self):

        file = json.loads(request.data)

        oid = ObjectId(file['_id'])
        description = file['description']

        if oid:
            if is_in_collection(oid, file_collection):
                file_collection.update_one({'_id' : oid},{"$set": {"description" : description}}, False)
                return Response(status=200, mimetype='application/json')
            else:
                raise BadRequest("File with that ObjectId not in database")
        else:
            raise BadRequest("No ObjectId specified, cannot update file entry")

        
    @auth.login_required
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
                
#List endpoint
#Responsible for: retreving a list of files
class List(Resource):
    @auth.login_required
    def get(self):

        search_query = request.args.get("query")
        serach_types = request.args.getlist("type")
        search_extentions = request.args.getlist("ext")
        search_case_sensitive = request.args.getlist("case")

        query_object = build_search_qeuery(search_query, serach_types, search_extentions, search_case_sensitive)
        file_list = list(file_collection.find(query_object))
    
        return  prep_file_list_for_json(file_list)
        
