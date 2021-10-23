from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from flaskr.app import create_app
from .modelos import db
from .vistas import VistaSignIn, VistaLogIn, VistaTasks, VistaTaskDetail, VistaFileDetail

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
    app.run(host='0.0.0.0', debug=True)
