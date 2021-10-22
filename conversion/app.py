from conversion import create_app
from flask_restful import Api

from .vistas import VistaFiles
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaFiles, '/files')

jwt = JWTManager(app)