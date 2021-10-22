from flask import Flask
from celery import Celery

UPLOAD_FOLDER = 'uploaded'
DOWNLOAD_FOLDER = 'download'

celery = Celery(__name__, broker='redis://localhost:6379/0')

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jimmy.orjuela:admin@localhost:5432/test"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app