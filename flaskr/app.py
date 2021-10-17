from flask import Flask
# from .app import create_app
from flask_restful import Api
#from .modelos import db
# from .vistas import VistaFiles
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from vistas import VistaFiles

UPLOAD_FOLDER = 'uploaded'
DOWNLOAD_FOLDER = 'download'


def create_app(config_name):
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sbbzmftwcpqmbs:63d510222da8ee4b0f412e7b34cd5b203ef12907f963453b33dec8f9f2169a0d@ec2-18-215-44-132.compute-1.amazonaws.com/d5h5dmuoe660fa'
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

# db.init_app(app)
# db.create_all()
cors = CORS(app)

api = Api(app)
api.add_resource(VistaFiles, '/files')
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
