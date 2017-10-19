from constants import *

#convert values in the file objects that JSON cannot serialze
def serialize_file_list(file_list):
        for f in file_list:
            f['_id'] = str(f['_id'])
            f['date_created'] = str(f['date_created'])

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

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS