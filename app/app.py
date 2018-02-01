import os
import boto3
import botocore
from flask import Flask, session, render_template, request, send_from_directory, url_for, redirect
import logging
from logging.handlers import RotatingFileHandler
import json
from subprocess import call

import eeg
import fmri

import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from lemur import datasets as lds, metrics as lms, plotters as lpl, embedders as leb

app = Flask(__name__)

app.debug = True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

MEDA_options = {
    'pheno': [
        #'NameOfPlotInLemur': 'name-of-plot-file-name'
        ('Heatmap', 'Heatmap', 'heatmap'),
        ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheatmap'),
        ('Location Lines', 'LocationLines', 'locationlines'),
        ('Location Heatmap', 'LocationHeatmap', 'locationheatmap'),
        ('Scree Plot', 'ScreePlotter', 'screeplot')
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
}

# EEG
One_to_One = [
    ('Connected Scatter', 'ConnectedScatter', 'connectedscatter'),
    ('Sparkline', 'Sparkline', 'sparkline'),
    ('Spatial Connection', 'SpatialConnection', 'spatialconn'),
]

EEG_Embed = [
   #'NameOfPlotInLemur': 'name-of-plot-file-name'
   ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
   ('Heatmap', 'Heatmap', 'heatmap'),
   ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
   ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
   ('Location Lines', 'LocationLines', 'locationlines'),
   ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
   ('Scree Plot', 'ScreePlotter', 'scree')
]

# Used for phenotypic
MEDA_Embedded_options = [
    ('Heatmap', 'Heatmap', 'embheatmap'),
    ('Histogram Heatmap', 'HistogramHeatmap', 'embhistogramheatmap'),
    ('Location Lines', 'LocationLines', 'emblocationlines'),
    ('Location Heatmap', 'LocationHeatmap', 'emblocationheatmap'),
    ('Scree Plot', 'ScreePlotter', 'embscreeplot'),
    ('Correlation Matrix', 'CorrelationMatrix', 'embcorr'),
    ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'embevheat'),
    ('HGMM Stacked Cluster Means Heatmap',
     'HGMMStackedClusterMeansHeatmap',
     'hgmmstackedclustermeansheatmap'),
    ('HGMM Cluster Means Dendrogram',
     'HGMMClusterMeansDendrogram',
     'hgmmclustermeansdendrogram'),
    ('HGMM Pairs Plot',
     'HGMMPairsPlot',
      'hgmmpairsplot'),
    ('HGMM Cluster Means Level Lines',
     'HGMMClusterMeansLevelLines',
      'hgmmclustermeanslevellines'),
    ('HGMM Cluster Means Level Heatmap',
     'HGMMClusterMeansLevelHeatmap',
     'hgmmclustermeanslevelheatmap'),
]

# fMRI
fmri_One_to_One = [
    ('Time Elapse of fMRI Signal', 'TimeElapse', 'orth_epi'),
]

@app.route('/')
def index():
    return redirect(url_for('medahome'))

@app.route('/MEDA/home')
def medahome():
    basedir = os.path.join(APP_ROOT, 'data')
    datasets = [di for di in os.listdir(basedir) if os.path.isdir(os.path.join(basedir, di))]
    metas = []
    eegs = []
    fmris = []
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
    return render_template('home.html', metas = metas, eegs = eegs, fmris = fmris)

@app.route('/MEDA/upload')
def uploadrender():
    return render_template("upload.html")

@app.route('/MEDA/plot/<ds_name>/pheno/<plot_name>')
def meda_pheno(ds_name=None, plot_name=None):
    app.logger.info('DS Name is: %s', ds_name)
    app.logger.info('Plot Name is: %s', plot_name)

    base_path = os.path.join(APP_ROOT, 'data', ds_name, 'pheno')

    if plot_name == "default":
        todisp = "<h1> Choose a plot! </h1>"
    elif plot_name is not None:
        plot_filename = "%s.html"%(plot_name)
        plot_path = os.path.join(base_path, plot_filename)
        with open(plot_path, "r") as f:
            todisp = f.read()
    else:
        todisp = "<h1> Choose a plot! </h1>"

    return render_template('meda_pheno.html',
                           plot=todisp,
                           total_plots={
                               'MEDA Options': MEDA_options['pheno'],
                               'MEDA Embedded Options': MEDA_Embedded_options
                                       }
                           )

@app.route('/MEDA/plot/<ds_name>/eeg/<mode>/<plot_name>')
def meda_eeg(ds_name=None, mode=None, plot_name=None):
    app.logger.info('DS Name is: %s', ds_name)
    app.logger.info('Plot Name is: %s', plot_name)
    subj_name = request.args.get('subj_name')
    test_name = request.args.get('test_name')
    if mode == 'embed':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, 'eeg_embedded_deriatives', 'agg')
    elif mode == 'one' and subj_name == 'none':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, 'eeg_derivatives')
    elif mode == 'one':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, 'eeg_derivatives', subj_name, test_name)
    else:
        base_path = os.path.join(APP_ROOT, 'data', ds_name, 'eeg_derivatives', 'agg')

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
        todisp = None
    elif plot_name is not None:
        plot_filename = "%s.html"%(plot_name)
        plot_path = os.path.join(base_path, plot_filename)
        with open(plot_path, "r") as f:
            todisp = f.read()
    else:
        todisp = "<h1> Choose a plot! </h1>"

    plot_title = ""
    if mode == "one":
        for title, _, tag in One_to_One:
            if tag == plot_name: plot_title = title

    return render_template('meda_eeg.html',
                           interm=zip(subjs, tasks),
                           one_title=plot_title,
                           plot=todisp,
                           MEDA_options = MEDA_options['eeg'],
                           MEDA_Embedded_options = EEG_Embed,
                           One_to_One = One_to_One
                       )

@app.route('/MEDA/plot/<ds_name>/fmri/<mode>/<plot_name>')
def meda_fmri(ds_name=None, mode=None, plot_name=None):
    app.logger.info('DS Name is: %s', ds_name)
    app.logger.info('Plot Name is: %s', plot_name)
    subj_name = request.args.get('subj_name')
    test_name = request.args.get('test_name')

    if mode == 'embed':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, 'fmri_embedded_deriatives', 'agg')
    elif mode == 'one' and subj_name == 'none':
        base_path = os.path.join(APP_ROOT, 'data', ds_name, 'fmri_derivatives')
    elif mode == 'one':
        base_path = os.path.join(ds_name, 'fmri_derivatives', subj_name, 'Nifti4DPlotter', test_name)
    else:
        base_path = os.path.join(APP_ROOT, 'data', ds_name, 'fmri_derivatives', 'agg')

    subjs = []
    tasks = []
    if plot_name == "default":
        todisp = "<h1> Choose a plot! </h1>"
    elif subj_name == "none" and mode == 'one':
        subjs = [di for di in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, di))
                 and di.startswith('sub')]
        tasks = []
        for subj in subjs:
            tasks.append([task_di for task_di in os.listdir(os.path.join(base_path, subj, 'Nifti4DPlotter'))
                          if os.path.isdir(os.path.join(base_path, subj, 'Nifti4DPlotter', task_di))])
        todisp = None
    elif plot_name is not None and mode == "one":
        plot_filename = "%s.gif"%(plot_name)
        plot_path = os.path.join(base_path, plot_filename)
        todisp = '<img src="%s" />'%(plot_path)
    elif plot_name is not None:
        plot_filename = "%s.html"%(plot_name)
        plot_path = os.path.join(base_path, plot_filename)
        with open(plot_path, "r") as f:
            todisp = f.read()
    else:
        todisp = "<h1> Choose a plot! </h1>"

    plot_title = ""
    if mode == "one":
        for title, _, tag in fmri_One_to_One:
            if tag == plot_name: plot_title = title

    return render_template('meda_fmri.html',
                           interm=zip(subjs, tasks),
                           one_title=plot_title,
                           plot=todisp,
                           MEDA_options = MEDA_options['eeg'],
                           MEDA_Embedded_options = EEG_Embed,
                           One_to_One = fmri_One_to_One
                       )


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT,'data')
    app.logger.info('Target route: %s', target)

    filedir = request.form['dataset-name']
    dspath = os.path.join(target, filedir)
    os.makedirs(dspath, exist_ok=True)
    session['basepath'] = dspath
    print(dspath)

    file_names = ['pheno', 'eeg', 'fmri']
    for file, name in zip(request.files.getlist("file"), file_names):
        if file.filename != '':
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

    if session['pheno_data'] is not None:
        # Create the dataset object
        csv_ds = lds.CSVDataSet(session['pheno_data'], name = filedir)

        # Clean the dataset object
        csv_ds.imputeColumns("mean")

        # Save metadata
        csv_ds.saveMetaData(os.path.join(dspath, "metadata.json"))

        # Create a lemur distance matrix based on the EEG data
        DM = lds.DistanceMatrix(csv_ds, lms.VectorDifferenceNorm)

        # Compute an embedding for the more intensive plots
        MDSEmbedder = leb.MDSEmbedder(num_components=3)
        csv_embedded = MDSEmbedder.embed(DM)
        phenopath = os.path.join(dspath, 'pheno')
        for _, lemurname, plotname in MEDA_options['pheno']:
            tosave = getattr(lpl, lemurname)(csv_ds, mode='div').plot()
            plotfilename = "%s.html"%(plotname)
            plotpath = os.path.join(phenopath, plotfilename)
            with open(plotpath, "w") as f:
                app.logger.info('Writing to file: %s', plotfilename)
                f.write(tosave)
                f.close()

        for _, lemurname, plotname in MEDA_Embedded_options:
            tosave = getattr(lpl, lemurname)(csv_embedded, mode='div').plot()
            plotfilename = "%s.html"%(plotname)
            plotpath = os.path.join(phenopath, plotfilename)
            with open(plotpath, "w") as f:
                app.logger.info('Writing to file: %s', plotfilename)
                f.write(tosave)
                f.close()

    if session['eeg_data'] is not None:
        # Download EEG patients
        app.logger.info("Downloading EEG Data...")
        credential_info = open(session['eeg_data'], 'r').read()
        bucket_name = credential_info.split(",")[0]
        cmd = ["aws", "s3",
               "cp", "s3://%s/eeg"%(bucket_name),
               os.path.join(session['basepath'], 'eeg'), "--recursive"]
        app.logger.info("EEG Data Downloaded")
        call(cmd)

        # Make plots
        eeg.run_eeg(os.path.basename(session['basepath']))

    if session['fmri_data'] is not None:
        # Download EEG patients
        app.logger.info("Downloading fMRI Data...")
        credential_info = open(session['fmri_data'], 'r').read()
        bucket_name = credential_info.split(",")[0]
        cmd = ["aws", "s3",
               "cp", "s3://%s/fmri"%(bucket_name),
               os.path.join(session['basepath'], 'fmri'), "--recursive"]
        app.logger.info("fMRI Data Downloaded")
        call(cmd)

        # Make plots
        fmri.run_fmri(os.path.basename(session['basepath']))

    if session['eeg_data'] is not None:
        return redirect(url_for('meda_eeg', ds_name=filedir, mode='none', plot_name='default'))
    if session['fmri_data'] is not None:
        return redirect(url_for('meda_fmri', ds_name=filedir, mode='none', plot_name='default'))
    return redirect(url_for('meda_pheno', ds_name=filedir, mode='none', plot_name='default'))

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
