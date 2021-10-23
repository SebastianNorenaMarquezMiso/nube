import datetime
import os
import subprocess as sp

from celery import Celery
from celery.signals import task_postrun
from flask import current_app

from app import db
from modelos import Task, TaskSchema

task_schema = TaskSchema()

app = Celery('tasks', broker='redis://redis:6379/0')
print("****")
print(app)

@app.task(name="tabla.file_conversion")
def file_conversion(request_json):
    # Build input path and add file
    print("1")
    inputF = os.path.join(
        os.path.dirname(__file__).replace("tareas", "") + current_app.config['UPLOAD_FOLDER'],
        request_json["filename"])
    print("2")
    # Build output path and add file
    outputF = os.path.join(
        os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'], request_json["dfile"])
 
    # Ffmpeg is flexible enough to handle wildstar conversions
    # convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    # convertCMD = ['/usr/bin/ffmpeg', '-y', '-i', inputF, outputF]
    print("3")
    convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    print("4")
    executeOrder66 = sp.Popen(convertCMD)
    print("5")
    try:
        outs, errs = executeOrder66.communicate(
            timeout=10)  # tell program to wait
    except TimeoutError:
        proc.kill()

    print("DONE\n")

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
    inputF = os.path.join(os.path.dirname(__file__).replace("tareas", "") + current_app.config['UPLOAD_FOLDER'],
                          request_json["filename"])  # Build input path
    outputF = os.path.join(os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'],
                           request_json["dfile"])  # Build output path

    # Ffmpeg is flexible enough to handle wildstar conversions
    # convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    # convertCMD = ['/usr/bin/ffmpeg', '-y', '-i', inputF, outputF]
    convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    executeOrder66 = sp.Popen(convertCMD)

    try:
        outs, errs = executeOrder66.communicate(timeout=10)  # tell program to wait
    except TimeoutError:
        proc.kill()

    # Delete previous file
    if request_json["status"] == "PROCESSED":
        previousName = request_json['nameFormat']
        outputF = os.path.join(os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'],
                               previousName)  # Build previous path
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
