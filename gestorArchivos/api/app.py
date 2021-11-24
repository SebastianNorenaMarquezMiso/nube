import os

from flask import Flask, render_template, request, redirect, send_file, url_for

from manages3 import download_file, upload_file


app = Flask(__name__)
BUCKET = "grupo5-files"


@app.route("/upload", methods=['POST'])
def postUpload():
    if request.method == "POST":
        f = request.files['file']
        f.save(f.filename)
        upload_file('uploads' , f"{f.filename}", BUCKET)
    return "Files updated", 200

@app.route("/upload/<filename>", methods=['GET'])
def getUpload(filename):
    if request.method == 'GET':
        return download_file('uploads' ,filename, BUCKET)
        
@app.route("/download", methods=['POST'])
def postDownload():
    if request.method == "POST":
        f = request.files['file']
        f.save(f.filename)
        upload_file('downloads',f"{f.filename}", BUCKET)
    return "Files updated", 200

@app.route("/download/<filename>", methods=['GET'])
def getDownload(filename):
    if request.method == 'GET':
        return download_file('downloads' ,filename, BUCKET)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=81)
