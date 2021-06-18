'''from flask import *
app = Flask(__name__, template_folder='template')
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template("hello.html")
if(__name__=='__main__'):
    app.run(debug='true')'''
import os
import botocore
from flask import Flask, render_template, request, redirect, send_file
#from s3_demo import list_files, download_file, upload_file
import boto3
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
    s3 = boto3.resource('s3')
    contents = []
    '''for item in s3.list_objects(Bucket=bucket)['contents']:
        contents.append(item)'''
    for item in s3.buckets.all():
        contents.append(item.name)
    return contents
app = Flask(__name__)
UPLOAD_FOLDER = "flask"
BUCKET = "hasramtan123"

@app.route('/')
def entry_point():
    return 'Hello World!'

@app.route("/storage")
def storage():
    contents = list_files("hasramtan123")
    return render_template('storage.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    s3=boto3.resource('s3')
    s3.create_bucket(Bucket='reciption',CreateBucketConfiguration={'LocationConstraint':'ap-south-1'})
    bucket=s3.Bucket('reciption')
    bucket.Acl().put(ACL='public-read')
'''def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return redirect("/storage")'''
@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
