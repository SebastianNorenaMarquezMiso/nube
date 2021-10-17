from flask import request, send_from_directory, current_app
import json
import os
from os import path
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask.json import jsonify
from werkzeug.utils import secure_filename
import subprocess as sp


FFMPEG_BIN = "ffmpeg.exe"
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'ogg', 'aac', 'wma'])


class VistaFiles(Resource):

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
            format = request.form.get("fileType")
            print(format)
            if str(format) in ALLOWED_EXTENSIONS:
                filename = secure_filename(file.filename)
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename))
                dfile = '{}.{}'.format(os.path.splitext(filename)[
                                       0], str(format))  # Build file name
                inputF = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename)  # Build input path
                # Build output path and add file
                outputF = os.path.join(
                    current_app.config['DOWNLOAD_FOLDER'], dfile)
                # Ffmpeg is flexible enough to handle wildstar conversions
                convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]

                executeOrder66 = sp.Popen(convertCMD)

                try:
                    outs, errs = executeOrder66.communicate(
                        timeout=10)  # tell program to wait
                except TimeoutError:
                    proc.kill()
                print("DONE\n")
                resp = jsonify({'message': os.path.join(current_app.config['UPLOAD_FOLDER'], filename)})
                resp.status_code = 201
                ddir = os.path.join(current_app.root_path,
                                    current_app.config['DOWNLOAD_FOLDER'])
                send_from_directory(
                    directory=ddir, filename=dfile, as_attachment=True)
                return resp

        else:
            resp = jsonify(
                {'message': 'Allowed file types are mp3, wav, ogg ,aac ,wma'})
            resp.status_code = 400
            return resp

    def get(self):
        return 'Funcionando'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
