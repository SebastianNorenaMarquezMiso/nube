from flask_jwt_extended import JWTManager
from flask_restful import Api

from flaskr import create_app
from .modelos import db
from .vistas import VistaFiles, VistaUpdateFiles, VistaDeleteFiles, VistaGetFiles

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaFiles, '/files')
api.add_resource(VistaGetFiles, '/get-files/<filename>')
api.add_resource(VistaUpdateFiles, '/update-files')
api.add_resource(VistaDeleteFiles, '/delete-files')

jwt = JWTManager(app)
