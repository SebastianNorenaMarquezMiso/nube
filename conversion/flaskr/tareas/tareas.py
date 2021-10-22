import datetime
import os
import subprocess as sp

from celery import Celery
from celery.signals import task_postrun
from flask import current_app

from ..app import db
from ..modelos import Task, TaskSchema

task_schema = TaskSchema()

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task(name="tabla.file_conversion")
def file_conversion(request_json):
    # Build input path and add file
    inputF = os.path.join(
        os.path.dirname(__file__).replace("tareas", "") + current_app.config['UPLOAD_FOLDER'],
        request_json["filename"])

    # Build output path and add file
    outputF = os.path.join(
        os.path.dirname(__file__).replace("tareas", "") + current_app.config['DOWNLOAD_FOLDER'], request_json["dfile"])

    # Ffmpeg is flexible enough to handle wildstar conversions
    # convertCMD = ['ffmpeg', '-y', '-i', inputF, outputF]
    # convertCMD = ['/usr/bin/ffmpeg', '-y', '-i', inputF, outputF]
    convertCMD = ['/usr/local/Cellar/ffmpeg/4.4_2/bin/ffmpeg', '-y', '-i', inputF, outputF]
    executeOrder66 = sp.Popen(convertCMD)

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


@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()
