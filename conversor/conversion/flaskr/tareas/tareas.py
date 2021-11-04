import datetime
import os
import subprocess as sp

from celery import Celery
from celery.signals import task_postrun
from flask import current_app

from app import db
from modelos import Task, TaskSchema
import requests

task_schema = TaskSchema()

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.conf.update(os.environ.items())
@app.task(name="tabla.file_conversion")
def file_conversion(request_json):
    # Build input path and add file
    # inputF = os.path.join(
    #     os.path.dirname(__file__).replace("tareas", "") + current_app.config['UPLOAD_FOLDER'],
    #     request_json["filename"])
    # Build output path and add file
    outputF = os.path.join(
         os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'], request_json["dfile"])
    inputF=os.getenv('URL_ARCHIVOS')+'/upload/' + request_json["filename"]

 
    # Ffmpeg is flexible enough to handle wildstar conversions
    # convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    convertCMD = ['/usr/bin/ffmpeg', '-y', '-i', inputF, outputF]
    # convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    executeOrder66 = sp.Popen(convertCMD)
    try:
        outs, errs = executeOrder66.communicate(
            timeout=10)  # tell program to wait
    except TimeoutError:
        proc.kill()

    print("DONE\n")
    #send download file to s3 and delete from local
    #upload file
    fileUp = open(os.path.join(
         os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'], request_json["filename"]), "rb")
    sendFileUp = {"file": fileUp}
    requests.post(os.getenv('URL_ARCHIVOS')+'/upload',
                                files=sendFileUp)
    os.remove(os.path.join(
         os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'], request_json["filename"]))
    
    #download file
    file = open(os.path.join(
         os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'], request_json["dfile"]), "rb")
    sendFile = {"file": file}
    
    requests.post(os.getenv('URL_ARCHIVOS')+'/download',
                                files=sendFile)
    outputFormat = os.path.join(current_app.config['DOWNLOAD_FOLDER'],
                                    request_json["dfile"])  # Build previous format name path
    os.remove(outputF)
    # Update DB
    task = Task.query.get_or_404(request_json["taskId"])
    task.name = request_json["filename"]
    task.status = "PROCESSED"
    task.nameFormat = request_json["dfile"]
    task.dateUp = task.dateUp
    ts2 = datetime.datetime.now()
    task.datePr = ts2
    db.session.commit()


@app.task(name="tabla.file_update")
def file_update(request_json):
    inputF=os.getenv('URL_ARCHIVOS')+'/upload/' + request_json["filename"]  # Build input path
    outputF = os.path.join(os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'],
                           request_json["dfile"])  # Build output path

    # Ffmpeg is flexible enough to handle wildstar conversions
    # convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    convertCMD = ['/usr/bin/ffmpeg', '-y', '-i', inputF, outputF]
    # convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    executeOrder66 = sp.Popen(convertCMD)

    try:
        outs, errs = executeOrder66.communicate(timeout=20)  # tell program to wait
    except TimeoutError:
        proc.kill()

    # Delete previous file
    if request_json["status"] == "PROCESSED":
        previousName = request_json['nameFormat']
        # outputF = os.path.join(os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'],
        #                        previousName)  # Build previous path
        # os.remove(outputF)
        
        #send download file to s3 and delete from local
    
        file = open(os.path.join(
            os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'], request_json["dfile"]), "rb")
        sendFile = {"file": file}
        requests.post(os.getenv('URL_ARCHIVOS')+'/download',
                                    files=sendFile)
        outputFormat = os.path.join(current_app.config['DOWNLOAD_FOLDER'],
                                        request_json["dfile"])  # Build previous format name path
        os.remove(outputF)

    print("DONE\n")

    task = Task.query.get_or_404(request_json["taskId"])
    task.status = "PROCESSED"
    task.datePr = datetime.datetime.now()
    task.nameFormat = request_json["dfile"]

    db.session.commit()


@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()
