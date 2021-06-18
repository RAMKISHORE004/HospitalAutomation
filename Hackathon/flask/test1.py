import os
from flask import Flask, render_template, request, redirect, send_file
import boto3
#from s3_demo import list_files, download_file, upload_file
def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response
def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)
    return output
def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)
    return contents
app = Flask(__name__, template_folder='template')
UPLOAD_FOLDER = "flask"
BUCKET = "reciption"

@app.route('/')
def entry_point():
    return 'Hello World!'

@app.route("/storage")
def storage():
    contents = list_files("reciption")
    #return render_template('storage.html', contents=contents)
    return '''
<!DOCTYPE html>
<html>
  <head>
    <title>FlaskDrive</title>
  </head>
  <body>
    <div class="content">
        <h3>Flask Drive: S3 Flask Demo</h3>
        <p>Welcome to this AWS S3 Demo</p>
        <div>
          <h3>Upload your file here:</h3>
          <form method="POST" action="/upload" enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
          </form>
        </div>
        <div>
          <h3>These are your uploaded files:</h3>
          <p>Click on the filename to download it.</p>
          <ul>
            {% for item in contents %}
              <li>
                <a href="/download/{{ item.Key }}"> {{ item.Key }} </a>
              </li>
            {% endfor %}
          </ul>
        </div>
    </div>
  </body>
</html>'''

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return redirect("/storage")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
