from flask import request, send_from_directory, current_app
import json
import os
from flask_restful import Resource, marshal_with, fields
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask.json import jsonify
from werkzeug.utils import secure_filename
from ..modelos import db, User, Task, UserSchema, TaskSchema
import subprocess as sp
import requests
import datetime
import asyncio

user_schema = UserSchema()
task_schema = TaskSchema()


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
        identity = get_jwt_identity()
        query_string = "select  * from task t where t.user =" + \
            str(identity)
        result = db.engine.execute(query_string)
        return [dict(row) for row in result]

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        f = request.files['file']
        format = request.form.get("newFormat")
        sendFile = {"file": (f.filename, f.stream, f.mimetype)}
        values = {'fileType': format}
        ts = datetime.datetime.now()
        # print(identity)
        new_task = Task(name=f.filename, status="UPLOADED",
                        dateUp=ts, datePr=ts, user=identity)
        db.session.add(new_task)
        db.session.commit()
        content = requests.post('http://127.0.0.1:5001/files',
                                files=sendFile, data=values)
        if(content.status_code == 201):
            task = Task.query.get_or_404(task_schema.dump(new_task)['id'])
            task.name =  task.name
            task.status = "PROCESSED"
            task.dateUp = task.dateUp
            ts2 = datetime.datetime.now()
            task.datePr =  ts2
            db.session.commit()
            return "Tasks converted", 200
        else:
            return "Tasks not converted", 400


class VistaTaskDetail(Resource):

    @jwt_required()
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task_schema.dump(task)

    @jwt_required()
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        return "Task updated", 200

    @jwt_required()
    def delete(self):
        return "Task deleted", 200


class VistaFileDetail(Resource):

    @jwt_required()
    def get(self, file_name):
        return "File detail", 200
