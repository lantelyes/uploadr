from constants import *
import glob, os, textract
from datetime import datetime
from flask_httpauth import HTTPDigestAuth
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

#create the file storage directory if it does not exist
def create_file_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

#Initialize the database
#Returns a reference to the collection object
def init_database_and_storage(collection_name):
    client = MongoClient()
    db = client.file_database
    if collection_name not in db.collection_names():
        db.create_collection(collection_name)

    file_collection = db.file_collection

    stored_files = get_stored_files()
    merge_existing_files_into_collection(stored_files,  file_collection)

    create_file_directory(UPLOAD_FOLDER)

    return file_collection

#Get a list of all the files in our upload directory
def get_stored_files():
    pdfs = glob.glob(UPLOAD_FOLDER + "*.pdf")
    docs = glob.glob(UPLOAD_FOLDER + "*.doc")
    docxs = glob.glob(UPLOAD_FOLDER + "*.docx")

    paths = pdfs + docs + docxs
    filenames =[os.path.basename(x) for x in paths]

    return filenames

#Merge a list of file names into the collection if missing
def merge_existing_files_into_collection(new_files, collection):

    for filename in new_files:
        if filename and is_allowed_file(filename):
            name = filename.rsplit('.', 1)[0]
            path = os.path.join(UPLOAD_FOLDER, filename)
            ext = filename.rsplit('.', 1)[1].lower()
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

            if not is_filename_in_collection(name, collection):
                collection.insert_one(file_data)
        else:
            print "Filename Invalid or file is wrong type"


#Check if a given file is already in the collection
#this checks against the name, this is less robust but we dont allow duplicate names so it should be ok
def is_filename_in_collection(filename, collection):

    if not filename:
        print "ERROR, invalid OID"
        return False
    if not collection:
        print "ERROR, invalid collection"
    else:
        return collection.find({'name' : filename}).count() == 1




#Check if a given file is already in the collection
#This checks against the ObjectId
def is_file_in_collection(file, collection):

    if not file:
        print "ERROR, invalid OID"
        return False
    if not collection:
        print "ERROR, invalid collection"
    else:
        oid = ObjectId(file["_id"])
        # we can assume the count wont be more than one as two objects cant have the same ObjectId
        return collection.find({'_id' : oid}).count() == 1

#Simple authentication functions
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


#Prep values in the file objects that JSON cannot serialze
def prep_file_list_for_json(file_list):
        for file in file_list:
            file['_id'] = str(file['_id'])
            file['date_created'] = str(file['date_created'])
            #Clear out the text data as we use the database for searching and dont need to send all that data back to the client
            file['text'] = ""

        return file_list

#build a search query based on parameters passed in on the request  
#this is very hacky, but it works for prototype purposes
def build_search_qeuery(query, types, extentions,case_sensitive):

    query_object =  {"$and": []}

    main_query = {"$or": []}
    regex_options = "i"

    if case_sensitive:
        regex_options = ""

    if extentions:
        ext_query = {"$or" : []}
        for ext in extentions:
            ext_query["$or"].append({"extention": ext})
        query_object["$and"].append(ext_query)

    name_query = {"name":  {'$regex': query, "$options" : regex_options} }
    contents_query = {"text":  {'$regex': query, "$options" : regex_options} }
    if "name" not in types and "contents" not in types:
        main_query["$or"].append(name_query)
        main_query["$or"].append(contents_query)

    if "name" in types:
        main_query["$or"].append(name_query)

    if "contents" in types:

        main_query["$or"].append(contents_query)

    if len(main_query["$or"]) != 0:
        query_object["$and"].append(main_query)

    return query_object


#checks if the filename is one of the allowed extentions
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS