from flask import Flask,  Request
from flask import Flask, render_template
from flask_restful import Api
from models import *



app = Flask(__name__)
api = Api(app)




api.add_resource(File, '/file')
api.add_resource(List, '/list')
api.add_resource(Upload, '/upload')



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


