from flask import request
from pymongo import MongoClient
from flask_restful import Resource, Api
from flask_uploads import UploadSet, configure_uploads, patch_request_class
from datetime import datetime

client = MongoClient()
db = client.file_database
file_collection = db.file_collection


UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class File(Resource):

    def get(self):
        return "Hello, world"

    def post(self):

        name = request.args.get('name')
        size = 0

     #   file = request.files['file']
     #   if file and is_allowed_extention(file.filename):
      #      filename = secure_filename(filename)
      #      path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      #      file.save(path)
       #     size = size = os.stat(path).st_size

        #size = size = os.stat('/tmp/foo').st_size

        file_data = {
            'name': name,
            'size_in_Kb': size,
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
        
