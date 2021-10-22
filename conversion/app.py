from conversion import create_app
from flask_restful import Api

from .vistas import VistaFiles, VistaUpdateFiles, VistaDeleteFiles, VistaGetFiles
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaFiles, '/files')
api.add_resource(VistaGetFiles, '/get-files/<filename>')
api.add_resource(VistaUpdateFiles, '/update-files')
api.add_resource(VistaDeleteFiles, '/delete-files')

jwt = JWTManager(app)