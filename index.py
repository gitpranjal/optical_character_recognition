from flask import Flask,abort, render_template,request,redirect,url_for
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import toTextConvertor
import os
import json

app = Flask(__name__)
#run_with_ngrok(app)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods = ['GET','POST'])
def get_box_info():
    if request.method == 'POST':
        print("##########", request.get_json())
        return {"Koi Mil Gya": "Yes"}

    return render_template('index.html')


if __name__ == '__main__':
    app.run()