import os
import shutil
import botocore
from flask import Flask, session, render_template, request, send_from_directory, url_for, redirect
import logging
from logging.handlers import RotatingFileHandler
import json
from subprocess import Popen, call, PIPE
import pexpect

import eeg
import fmri
import pheno
import graph

import db.mongo_update as mongo_update

import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from lemur import datasets as lds, metrics as lms, plotters as lpl, embedders as leb

app = Flask(__name__)

app.debug = True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

aggregate_options = {
    'pheno': [
        #'NameOfPlotInLemur': 'name-of-plot-file-name'
        ('Heatmap', 'Heatmap', 'heatmap'),
        ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        ('Location Lines', 'LocationLines', 'locationlines'),
        ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        ('Scree Plot', 'ScreePlotter', 'scree')
    ],
    'eeg': [
        #'NameOfPlotInLemur': 'name-of-plot-file-name'
        ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        ('Heatmap', 'Heatmap', 'squareheat'),
        ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        ('Location Lines', 'LocationLines', 'locationlines'),
        ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        ('Scree Plot', 'ScreePlotter', 'scree')
    ],
    'fmri': [
        #'NameOfPlotInLemur': 'name-of-plot-file-name'
        ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        ('Heatmap', 'Heatmap', 'squareheat'),
        ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        ('Location Lines', 'LocationLines', 'locationlines'),
        ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        ('Scree Plot', 'ScreePlotter', 'scree')
    ],
    'graph': [
        #'NameOfPlotInLemur': 'name-of-plot-file-name'
        ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        ('Heatmap', 'Heatmap', 'squareheat'),
        ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        ('Location Lines', 'LocationLines', 'locationlines'),
        ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        ('Scree Plot', 'ScreePlotter', 'scree'),
        ('Graph Stats', 'GraphStats', 'gr_stats')
    ]
}

# EEG and FMRI One-to-One options.
one_to_one_options = {
    'pheno' : [
    ],
    'eeg' : [
        ('Connected Scatter', 'ConnectedScatter', 'connectedscatter'),
        ('Sparkline', 'Sparkline', 'sparkline'),
        ('Spatial Time Series', 'SpatialTimeSeries', 'spatialtimeseries'),
        ('Spatial Periodogram', 'SpatialPeriodogram', 'spatialpgram')
    ],
    'fmri' : [
        ('Time Elapse of fMRI Signal', 'TimeElapse', 'orth_epi')
    ],
    'graph' : []
}

# Embed for EEG and FMRI
embedded_options = {
    'pheno' : [
        ('Heatmap', 'Heatmap', 'heatmap'),
        ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        ('Location Lines', 'LocationLines', 'locationlines'),
        ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        ('Scree Plot', 'ScreePlotter', 'scree'),
        ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        ('HGMM Stacked Cluster Means Heatmap',
         'HGMMStackedClusterMeansHeatmap',
         'hgmmscmh'),
        ('HGMM Cluster Means Dendrogram',
         'HGMMClusterMeansDendrogram',
         'hgmmcmd'),
        ('HGMM Pairs Plot',
         'HGMMPairsPlot',
          'hgmmcpp'),
        ('HGMM Cluster Means Level Lines',
         'HGMMClusterMeansLevelLines',
          'hgmmcmll'),
        ('HGMM Cluster Means Level Heatmap',
         'HGMMClusterMeansLevelHeatmap',
         'hgmmcmlh')
    ],
    'eeg' : [
       #'NameOfPlotInLemur': 'name-of-plot-file-name'
       ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
       ('Heatmap', 'Heatmap', 'heatmap'),
       ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
       ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
       ('Location Lines', 'LocationLines', 'locationlines'),
       ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
       ('Scree Plot', 'ScreePlotter', 'scree')
    ],
    'fmri' : [
       #'NameOfPlotInLemur': 'name-of-plot-file-name'
       ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
       ('Heatmap', 'Heatmap', 'heatmap'),
       ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
       ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
       ('Location Lines', 'LocationLines', 'locationlines'),
       ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
       ('Scree Plot', 'ScreePlotter', 'scree')
    ],
    'graph' : [
        ('Heatmap', 'Heatmap', 'heatmap'),
        ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        ('Location Lines', 'LocationLines', 'locationlines'),
        ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        ('Scree Plot', 'ScreePlotter', 'scree'),
        ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        ('HGMM Stacked Cluster Means Heatmap',
         'HGMMStackedClusterMeansHeatmap',
         'hgmmscmh'),
        ('HGMM Cluster Means Dendrogram',
         'HGMMClusterMeansDendrogram',
         'hgmmcmd'),
        ('HGMM Pairs Plot',
         'HGMMPairsPlot',
          'hgmmcpp'),
        ('HGMM Cluster Means Level Lines',
         'HGMMClusterMeansLevelLines',
          'hgmmcmll'),
        ('HGMM Cluster Means Level Heatmap',
         'HGMMClusterMeansLevelHeatmap',
         'hgmmcmlh')
    ],
}

@app.route('/')
def index():
    return redirect(url_for('uploadrender'))

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/MEDA/datasets')
def medahome():
    basedir = os.path.join(APP_ROOT, 'data')
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    datasets = [di for di in os.listdir(basedir) if os.path.isdir(os.path.join(basedir, di))]
    metas = []
    eegs = []
    fmris = []
    graphs = []
    for d in datasets:
        print(os.path.join(basedir, d, "metadata.json"))
        if os.path.exists(os.path.join(basedir, d, "metadata.json")):

            with open(os.path.join(basedir, d, "metadata.json")) as f:
                rawjson = f.read()
            metadata = json.loads(rawjson)
            metas.append(metadata)
        if os.path.exists(os.path.join(basedir, d, 'eeg')):
            eegs.append(d)
        if os.path.exists(os.path.join(basedir, d, 'fmri')):
            fmris.append(d)
        if os.path.exists(os.path.join(basedir, d, 'graph')):
            graphs.append(d)
    return render_template('home.html', metas = metas, eegs = eegs, fmris = fmris, graphs = graphs)

# Delete dataset from app.
@app.route('/MEDA/datasets/delete/<dataset>')
def delete_dataset(dataset = None):
    datadir = os.path.join(APP_ROOT, 'data', dataset)
    shutil.rmtree(datadir+"/")
    return redirect(url_for('medahome'))

@app.route('/MEDA/home')
def uploadrender():
    return render_template("upload.html")

# Function currently plots EEG modality, but is a general purpose function for FMRI as well.
# TO DO: Check the differences between templates.
@app.route('/MEDA/plot/<ds_name>/<modality>/<mode>/<plot_name>')
def meda_modality(ds_name=None, modality=None, mode=None, plot_name=None):
    app.logger.info('DS Name is: %s', ds_name)
    app.logger.info('Plot Name is: %s', plot_name)
    try:
        subj_name = request.args.get('subj_name')
        test_name = request.args.get('test_name')
    except:
        subj_name = None
        test_name = None
    if mode == 'embed':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, modality+'_embedded_deriatives', 'agg')
    elif mode == 'one' and subj_name == 'none':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, modality+'_derivatives')
    elif mode == 'one':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, modality+'_derivatives', subj_name, test_name)
    else:
        base_path = os.path.join(APP_ROOT, 'data', ds_name, modality+'_derivatives', 'agg')

    subjs = []
    tasks = []
    if plot_name == "default":
        todisp = "<h1> Choose a plot! </h1>"
    elif subj_name == "none" and mode == 'one':
        subjs = [di for di in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, di))
                    and di.startswith('sub')]
        tasks = []
        for subj in subjs:
            tasks.append([task_di for task_di in os.listdir(os.path.join(base_path, subj))
                          if os.path.isdir(os.path.join(base_path, subj, task_di))])
            if modality == 'fmri':
                tasks.append([task_di for task_di in os.listdir(os.path.join(base_path, subj, 'Nifti4DPlotter'))
                              if os.path.isdir(os.path.join(base_path, subj, 'Nifti4DPlotter', task_di))])
        todisp = None
    elif plot_name is not None:
        plot_filename = "%s.html"%(plot_name)
        plot_path = os.path.join(base_path, plot_filename)
        with open(plot_path, "r") as f:
            todisp = f.read()
    else:
        todisp = "<h1> Choose a plot! </h1>"

    '''
    # To be incorporated  in the ABOVE IF-BLOCK with FMRI one-to-one plot.
    elif plot_name is not None and mode == "one":
        plot_filename = "%s.gif"%(plot_name)
        plot_path = os.path.join(base_path, plot_filename)
        todisp = '<img src="%s" />'%(plot_path)
    elif plot_name is not None: ...
    '''

    plot_title = ""
    if mode == "one":
        for title, _, tag in one_to_one_options[modality]:
            if tag == plot_name: plot_title = title

    return render_template('meda_modality.html',
                           interm=zip(subjs, tasks),
                           one_title=plot_title,
                           plot=todisp,
                           MEDA_options = aggregate_options[modality],
                           MEDA_Embedded_options = embedded_options[modality],
                           One_to_One = one_to_one_options[modality],
                           Modality = modality
                       )

# Pass modality as string, and base path.
def run_modality(modality, basepath):
    if modality == 'eeg':
        eeg.run_eeg(basepath)
    elif modality == 'fmri':
        fmri.run_fmri(basepath)
    elif modality == 'graph':
        graph.run_graph(basepath)

@app.route('/upload', methods=['POST'])
def upload():

    target = os.path.join(APP_ROOT,'data')
    app.logger.info('Target route: %s', target)

    filedir = request.form['dataset-name']
    dspath = os.path.join(target, filedir)
    os.makedirs(dspath, exist_ok=True)
    session['basepath'] = dspath
    # print(dspath)
    # print(request.files.getlist('file'))
    # print(request.files['file[]'])

    file_names = ['pheno', 'eeg', 'fmri', 'graph']

    for name in file_names:
        files = request.files.getlist(name)
        # app.logger.info('Input type: %s, File name: %s', name, file.filename)
        if len(files) != 0 and files[0].filename != '':
            file = files[0]
            app.logger.info('Input type in loop: %s', name)
            dirpath = os.path.join(dspath, name)
            os.makedirs(dirpath, exist_ok=True)
            filename = file.filename
            destination = os.path.join(dspath, filename)
            app.logger.info('Accept incoming file: %s', filename)
            app.logger.info('Save it to: %s', destination)
            file.save(destination)
            session[name + '_data'] = destination
        else:
            session[name + '_data'] = None

    # For modalities in which you upload S3 credentials.
    for name in ['eeg', 'fmri', 'graph']:
        if session[name+'_data'] is not None:
            # Download EEG patients
            app.logger.info("Downloading "+name+" Data...")

            # Collect AWS credentials,
            credential_info = open(session[name+'_data'], 'r').read().split(",")
            bucket_name = credential_info[0]
            ACCESS_KEY = str(credential_info[1])
            SECRET_KEY = str(credential_info[2])

            # Download files
            '''
            s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-east-1')
            bucket = s3.Bucket(bucket_name)
            for elem in bucket.list():
                key = elem.name.encode('utf-8')
                bucket.download_file(key, os.path.join(session['basepath'], name)+"/"+str(key.split('/')[-1]))
            '''

            # Configre AWS Credentials

            cmd = ["aws", "s3",
                   "cp", ("s3://%s/"+name)%(bucket_name),
                   os.path.join(session['basepath'], name), "--recursive"]
            app.logger.info(name+" Data Downloaded")
            call(cmd)

            mongo_update.build_database(filedir, bucket_name)


            run_modality(name, os.path.basename(session['basepath']))

    # For modalities in which you upload the dataset itself.
    if session['pheno_data'] is not None:
        pheno.run_pheno(session['pheno_data'])

    for name in file_names:
        if session[name+'_data'] is not None:
            return redirect(url_for('meda_modality', ds_name=filedir, modality=name, mode='none', plot_name='default'))

@app.route('/s3upload', methods=['POST'])
def s3upload():

    target = os.path.join(APP_ROOT,'downloads')
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

        credential_info = open(destination, 'r').readlines()
        bucket_name = credential_info[0][:-1]

        cmd = ["aws", "s3", "cp", "s3://%s/%s"%(bucket_name, )]
        # # Uploads the given file using a managed uploader, which will split up large
        # # files automatically and upload parts in parallel.
        client.upload_file(destination, bucket_name, filename)
        #
        # # Then grab the file from S3 bucket to show connection is established
        KEY = filename  # replace with your object key

        objects = client.list_objects(Bucket = bucket_name)['Contents']
        for s3_key in objects:
            s3_object = s3_key['Key']
            if not s3_object.endswith("/"):
                client.download_file(bucket_name, s3_object, target+'/'+ s3_object)
            else:
                if not os.path.exists(s3_object):
                    os.makedirs(target+'/'+ s3_object)


        try:
            client.download_file(bucket_name, KEY, KEY)
            app.logger.info('Downloading file from S3...')
            # s = open(filename, 'r')
            # print s.read()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                app.logger.error('The object does not exist.')
            else:
                raise
        #         # s = open(destination, 'r')
        #         # print s.read()
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
    app.run(host='0.0.0.0')
