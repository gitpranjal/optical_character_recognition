from flask import Flask,abort, render_template,request,redirect,url_for
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import toTextConvertor
import os

app = Flask(__name__)
run_with_ngrok(app)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] , filename))
            result_dict = toTextConvertor.return_dict(app.config['UPLOAD_FOLDER']+"/"+filename)
            os.remove(app.config['UPLOAD_FOLDER']+"/"+filename)
            return toTextConvertor.print_nested_dictionary(result_dict)
    return render_template('file_upload.html')


if __name__ == '__main__':
    app.run()