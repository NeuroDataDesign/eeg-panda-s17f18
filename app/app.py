import os
import boto3
import botocore
from flask import Flask, render_template, request, send_from_directory
import logging
from logging.handlers import RotatingFileHandler
from runner import get_pheno_plots

app = Flask(__name__)

app.debug = True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT,'data')
    # target = "/home/nitin/hopkins/fall2017/ndd/kpfv2/"
    app.logger.info('Target route: %s', target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        # print file
        filename = file.filename
        destination = "/".join([target,filename])
        file.save(destination)
        app.logger.info('Accept incoming file: %s', filename)
        app.logger.info('Save it to: %s', destination)
        app.logger.info('Starting phenotypic plots...')
        get_pheno_plots(target, destination)
        app.logger.info('... finishing phenotypic plots')
    return render_template("complete.html", file_name=filename)

@app.route('/s3upload', methods=['POST'])
def s3upload():
    target = os.path.join(APP_ROOT,'text')
    app.logger.info('Target route: %s', target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        # print file
        filename = file.filename
        destination = "/".join([target,filename])
        app.logger.info('Accept incoming file: %s', filename)
        app.logger.info('Save it to: %s', destination)
        file.save(destination)

        s3 = boto3.client('s3')
        bucket_name = 'lemurndd'

        # Uploads the given file using a managed uploader, which will split up large
        # files automatically and upload parts in parallel.
        s3.upload_file(destination, bucket_name, filename)

        # Then grab the file from S3 bucket to show connection is established
        s3 = boto3.resource('s3')
        KEY = filename  # replace with your object key

        try:
            s3.Bucket(bucket_name).download_file(KEY, KEY)
            app.logger.info('Downloading file from S3...')
            # s = open(filename, 'r')
            # print s.read()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                app.logger.error('The object does not exist.')
            else:
                raise
                # s = open(destination, 'r')
                # print s.read()
    return render_template("complete.html",file_name = filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("text", filename)

@app.route('/display/<filename>')
def display_file(filename):
    target = os.path.join(APP_ROOT,'text')
    destination = "/".join([target, filename])
    s = open(destination, 'r')
    # print(s.read())
    return render_template("home.html", file_name=filename)

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()