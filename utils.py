from constants import *
from flask_httpauth import HTTPDigestAuth

auth = HTTPDigestAuth()

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


#convert values in the file objects that JSON cannot serialze
def prep_file_list_for_json(file_list):
        for f in file_list:
            f['_id'] = str(f['_id'])
            f['date_created'] = str(f['date_created'])
            #Clear out the text data as we use the database for searching and dont need to send all that data back to the client
            f['text'] = ""

        return file_list

#build a search query based on parameters passed in on the request  
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
    
    if "name" in types:
        name_query = {"name":  {'$regex': query, "$options" : regex_options} }
        main_query["$or"].append(name_query)

    if "contents" in types:
        contents_query = {"text":  {'$regex': query, "$options" : regex_options} }
        main_query["$or"].append(contents_query)

    if len(main_query["$or"]) != 0:
        query_object["$and"].append(main_query)

    print query_object

    return query_object


#checks if the filename is one of the allowed extentions
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS