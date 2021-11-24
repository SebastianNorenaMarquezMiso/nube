from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

# from flaskr import create_app

from modelos import db
from vistas import VistaSignIn, VistaLogIn, VistaTasks, VistaTaskDetail, VistaFileDetail
UPLOAD_FOLDER = 'uploaded'
DOWNLOAD_FOLDER = 'download'


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://qjlyjzmhavutlb:2062db08854b1ce90b969530506391dac80654dce0ce0ddf35eb11cb96a8a218@ec2-44-196-71-136.compute-1.amazonaws.com:5432/d3e8q7im41jpie"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)

api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTaskDetail, '/api/tasks/<int:task_id>')
api.add_resource(VistaFileDetail, '/api/files/<string:file_name>')

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=80)
