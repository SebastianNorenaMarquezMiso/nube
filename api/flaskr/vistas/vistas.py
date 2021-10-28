import datetime
import io
import json

import requests
from flask import request, send_file
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource

from modelos import db, User, Task, UserSchema, TaskSchema

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
        query_string = "select * from task t where t.user =" + str(identity)
        result = db.engine.execute(query_string)
        return json.loads(json.dumps([dict(row) for row in result], default=myConverter))

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        f = request.files['file']
        format = request.form.get("newFormat")
        sendFile = {"file": (f.filename, f.stream, f.mimetype)}
        ts = datetime.datetime.now()
        new_task = Task(name=f.filename, status="UPLOADED",
                        dateUp=ts, datePr=ts, nameFormat="", user=identity)
        db.session.add(new_task)
        db.session.commit()

        values = {'fileType': format, 'taskId': task_schema.dump(new_task)['id']}

        content = requests.post(' http://3.93.36.145/files',
                                files=sendFile, data=values)
        if (content.status_code == 201):
            return "Tasks converted", 200
        else:
            return content.json(), 400


class VistaTaskDetail(Resource):

    @jwt_required()
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return json.loads(json.dumps(task_schema.dump(task), default=myConverter))

    @jwt_required()
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        taskJson = json.loads(json.dumps(task_schema.dump(task), default=myConverter))

        task.status = "UPLOADED"
        task.dateUp = datetime.datetime.now()
        db.session.commit()

        content = requests.put('http://3.93.36.145/update-files',
                               json={'name': taskJson['name'], 'status': taskJson['status']['llave'], 'taskId': task_id,
                                     'nameFormat': taskJson['nameFormat'], 'newFormat': request.form.get('newFormat')})

        if (content.status_code == 201):
            return "Task updated", 200
        else:
            return "Tasks not updated", 400

    @jwt_required()
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        taskJson = json.loads(json.dumps(task_schema.dump(task), default=myConverter))

        content = requests.delete('http://3.93.36.145/delete-files',
                                  json={'name': taskJson['name'], 'nameFormat': taskJson['nameFormat']})

        if (content.status_code == 200):
            db.session.delete(task)
            db.session.commit()
            return "Task deleted", 200
        else:
            return "Tasks not deleted", 400


class VistaFileDetail(Resource):

    @jwt_required()
    def get(self, file_name):
        content = requests.get('http://3.93.36.145/get-files/' + file_name, stream=True)
        return send_file(io.BytesIO(content.content), as_attachment=True, attachment_filename=file_name)


def myConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
