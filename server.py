# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:28:38 2017

@author: Ba La
"""
import os
from flask import Flask, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
app = Flask(__name__)
import logging
from detect import get_Number
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
UPLOAD_FOLDER = 'C:\\Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries1',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]
@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #TODO: Call the dectect.py function to do the NPR
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            code = get_Number(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if(len(code)>0):
                return jsonify({'Status': "Done",'Number':str(code)})
            else:
                return jsonify({"Status": "Not able to recognize the number ..."})
    return'''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    print(request)
    app.logger.info(str(request))
    app.logger.info(str(request.args))
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    #goto localhost:5000/upload
    app.run(debug=True)