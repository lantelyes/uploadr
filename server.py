from flask import Flask, Request, render_template
from flask_restful import Api
from api import *
from utils import *

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)
api.add_resource(File, '/file')
api.add_resource(List, '/list')
api.add_resource(Upload, '/upload')

@auth.get_password
def get_pw(username):
    if username in USERS:
        return USERS.get(username)
    return None

#Our main page
@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)