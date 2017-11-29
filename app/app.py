import sys, os
import boto3
import botocore
from flask import Flask, session, render_template, request, send_from_directory, url_for, redirect
import logging
from logging.handlers import RotatingFileHandler
from runner import get_pheno_plots

sys.path.append(os.path.abspath(os.path.join('..')))
from lemur import datasets as lds, metrics as lms, plotters as lpl, embedders as leb

app = Flask(__name__)

app.debug = True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/MEDA/<plot_name>')
def meda(plot_name=None):
    app.logger.info('Plot Name is: %s', plot_name)
    app.logger.info('CSV File is: %s', session['data'])
    pheno = lds.CSVDataSet(session['data'], name = "HBN Phenotypic")
    pheno.imputeColumns("mean")

    options = {
        'Heatmap': 'heatmap',
        'Location Heatmap': 'locheat',
        'Location Lines': 'loclines',
        'Histogram Heatmap': 'histheat',
        'Correlation Matrix': 'corr',
        'Scree Plot': 'scree',
        'Eigenvector Heatmap': 'eigen'
    }

    if plot_name == 'heatmap':
        todisp = lpl.Heatmap(pheno, mode='div').plot()
    elif plot_name == 'locheat':
        todisp = lpl.LocationHeatmap(pheno, mode='div').plot()
    elif plot_name == 'loclines':
        todisp = lpl.LocationLines(pheno, mode='div').plot()
    elif plot_name == 'histheat':
        todisp = lpl.HistogramHeatmap(pheno, mode='div').plot()
    elif plot_name == 'corr':
        todisp = lpl.CorrelationMatrix(pheno, mode='div').plot()
    elif plot_name == 'scree':
        todisp = lpl.ScreePlotter(pheno, mode='div').plot()
    elif plot_name == 'eigen':
        todisp = lpl.EigenvectorHeatmap(pheno, mode='div').plot()
    else:
        todisp = "<h1> Choose a plot! </h1>"
    return render_template('meda.html', plot=todisp, options=options)


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT,'data')
    app.logger.info('Target route: %s', target)

    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files.getlist("file")[0]
    # print file
    filename = file.filename
    destination = "/".join([target,filename])
    app.logger.info('Accept incoming file: %s', filename)
    app.logger.info('Save it to: %s', destination)
    file.save(destination)
    session['data'] = destination
    return redirect(url_for('meda', plot_name='heatmap'))

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