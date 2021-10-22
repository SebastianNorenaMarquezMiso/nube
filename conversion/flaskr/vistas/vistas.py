import os
import subprocess as sp
import time
import uuid

from celery import Celery
from flask import request, send_from_directory, current_app
from flask.json import jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename

FFMPEG_BIN = "ffmpeg.exe"
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'ogg', 'aac', 'wma'])

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task(name="tabla.file_conversion")
def file_conversion(request_json):
    pass


class VistaFiles(Resource):

    def post(self):
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        if 'fileType' not in request.form:
            resp = jsonify({'message': 'No newFormat part in the request'})
            resp.status_code = 400
            return resp

        file = request.files['file']

        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp

        if file and allowed_file(file.filename):
            format = request.form.get("fileType")

            filename = secure_filename(file.filename)
            filename = '{}.{}'.format(os.path.splitext(filename)[0] + str(uuid.uuid4()),
                                      os.path.splitext(filename)[1])  # Build input name
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            uuidSelected = uuid.uuid4()
            dfile = '{}.{}'.format(os.path.splitext(filename)[
                                       0] + str(uuidSelected), str(format))  # Build file name

            json = {
                'creation_date': str(int(time.time())),
                'filename': filename,
                'dfile': dfile,
                'taskId': request.form.get("taskId")
            }

            args = (json,)
            file_conversion.apply_async(args)

            resp = jsonify({
                'sourceFile': filename,
                'formatFile': dfile
            })
            resp.status_code = 201
            return resp

        else:
            resp = jsonify(
                {'message': 'Allowed file types are mp3, wav, ogg ,aac ,wma'})
            resp.status_code = 400
            return resp


class VistaGetFiles(Resource):
    def get(self, filename):
        try:
            return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename=filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)


class VistaUpdateFiles(Resource):

    def put(self):
        # Convert file
        name = request.json['name']
        newFormat = request.json['newFormat']
        status = request.json['status']

        dfile = '{}.{}'.format(os.path.splitext(name)[0] + str(uuid.uuid4()), str(newFormat))  # Build file name

        inputF = os.path.join(current_app.config['UPLOAD_FOLDER'], name)  # Build input path
        outputF = os.path.join(current_app.config['DOWNLOAD_FOLDER'], dfile)  # Build output path

        convertCMD = ['/usr/local/Cellar/ffmpeg/4.4_2/bin/ffmpeg', '-y', '-i', inputF, outputF]
        executeOrder66 = sp.Popen(convertCMD)

        try:
            outs, errs = executeOrder66.communicate(timeout=10)  # tell program to wait
        except TimeoutError:
            proc.kill()

        # Delete previous file
        if status == "PROCESSED":
            previousName = request.json['nameFormat']
            outputF = os.path.join(current_app.config['DOWNLOAD_FOLDER'], previousName)  # Build previous path
            os.remove(outputF)

        # Build response
        resp = jsonify({
            'sourceFile': inputF,
            'formatFile': dfile
        })
        resp.status_code = 201
        ddir = os.path.join(current_app.root_path, current_app.config['DOWNLOAD_FOLDER'])
        send_from_directory(directory=ddir, filename=dfile, as_attachment=True)
        return resp


class VistaDeleteFiles(Resource):

    def delete(self):
        name = request.json['name']
        nameFormat = request.json['nameFormat']
        outputF = os.path.join(current_app.config['UPLOAD_FOLDER'], name)  # Build previous name path
        outputFormat = os.path.join(current_app.config['DOWNLOAD_FOLDER'],
                                    nameFormat)  # Build previous format name path
        os.remove(outputF)
        os.remove(outputFormat)

        resp = jsonify(
            {'message': 'Files deleted'}
        )
        resp.status_code = 200
        return resp


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
