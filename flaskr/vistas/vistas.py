from flask import request
import json
import os
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask.json import jsonify
from werkzeug.utils import secure_filename

from flaskr.modelos import db, User, Task

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt'])


class VistaFiles(Resource):

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER))
            print(file)
            resp = jsonify({'message': 'File successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(
                {'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp

    def get(self):
        return 'Funcionando'

class VistaSignIn(Resource):

    def post(self):
        if request.json["password1"] != request.json["password2"]:
            return "Password do not match", 400
        else:
            new_user = User(
                username=request.json["username"], password=request.json["password1"], email=request.json["email"])
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=new_user.id)
            return {"message": "User created successfully", "token": access_token}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class VistaLogIn(Resource):

    def post(self):
        user = User.query.filter(
            User.username == request.json["username"], User.password == request.json["password"]).first()
        db.session.commit()
        if user is None:
            return "User not exit", 404
        else:
            token_de_acceso = create_access_token(identity=user.id)
            return {"message": "Successful login", "token": token_de_acceso}

class VistaTasks(Resource):

    @jwt_required()
    def get(self):
        return "Tasks", 200

    @jwt_required()
    def post(self):
        # request.json["fileName"]
        # request.json["newFormat"]
        return "Tasks converted", 200

class VistaTaskDetail(Resource):

    @jwt_required()
    def get(self, task_id):
        return "Task detail", 200

    @jwt_required()
    def put(self, task_id):
        # request.json["newFormat"]
        return "Task updated", 200

    @jwt_required()
    def delete(self):
        return "Task deleted", 200

class VistaFileDetail(Resource):

    @jwt_required()
    def get(self, file_name):
        return "File detail", 200