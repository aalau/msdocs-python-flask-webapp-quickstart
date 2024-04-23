import os
from transformers import pipeline
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
pipe_ingredients = pipeline("image-segmentation", model="prem-timsina/segformer-b0-finetuned-food")
pipe_name = pipeline("image-classification", model="nateraw/food")
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your_project_id.appspot.com'
}) # TODO: update this function with appropriate credentials

def upload_file_to_firebase(file_path, destination_blob_name):
    try:
        # Get a reference to the Firebase Storage bucket
        bucket = storage.bucket()

        # Create a blob object representing the file to upload
        blob = bucket.blob(destination_blob_name)

        # Upload the file to Firebase Storage
        blob.upload_from_filename(file_path)

        print(f"File uploaded to Firebase Storage: {destination_blob_name}")
        return True
    except Exception as e:
        print(f"Error uploading file to Firebase Storage: {e}")
        return False


app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods = ['PUT'])
def upload():
    if request.method == 'PUT':
        if 'file' not in request.files:
            return "No file selected"
    for file in request.files(file.filename):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save file
            #return jsonify(result) # return in json format


@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


if __name__ == '__main__':
   app.run()
