import os
import shutil
import pickle as pkl
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

import lemur.plotters as lpl

import db.mongo_update as mongo_update
import db.mongo_get as mongo_get

import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from lemur import datasets as lds, metrics as lms, plotters as lpl, embedders as leb

app = Flask(__name__)

app.debug = True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#'NameOfPlotInLemur': 'name-of-plot-file-name'
aggregate_options = {
    'pheno': {
        'heatmap': ('Heatmap', 'Heatmap', 'heatmap'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'eeg': {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'fmri': {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'graph': {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree'),
        'gr_stats': ('Graph Stats', 'GraphStats', 'gr_stats')
    }
}

# EEG and FMRI One-to-One options.
one_to_one_options = {
    'pheno' : {
    },
    'eeg' : {
        'connectedscatter': ('Connected Scatter', 'ConnectedScatter', 'connectedscatter'),
        'sparkline': ('Sparkline', 'Sparkline', 'sparkline'),
        'spatialtimeseries': ('Spatial Time Series', 'SpatialTimeSeries', 'spatialtimeseries'),
        'spatialpgram': ('Spatial Periodogram', 'SpatialPeriodogram', 'spatialpgram')
    },
    'fmri' : {
        'orth_epi': ('Time Elapse of fMRI Signal', 'TimeElapse', 'orth_epi')
    },
    'graph' : {
        'gr_stats': ('Graph Stats', 'GraphStats', 'gr_stats')
    }
}

# Embed for EEG and FMRI
embedded_options = {
    'pheno' : {
        'heatmap': ('Heatmap', 'Heatmap', 'heatmap'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat' : ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree' : ('Scree Plot', 'ScreePlotter', 'scree'),
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat')
    },
    'eeg' : {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'fmri' : {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'graph' : {
        'heatmap': ('Heatmap', 'Heatmap', 'heatmap'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    }
}

clustering_options = {
    'pheno' : {
        'hgmmscmh' : ('HGMM Stacked Cluster Means Heatmap',
                      'ClusterMeansLevelHeatmap',
                      'hgmmscmh'),
        'hgmmcmd' : ('HGMM Cluster Means Dendrogram',
                     'HierarchicalClusterMeansDendrogram',
                     'hgmmcmd'),
        'hgmmcpp' : ('HGMM Pairs Plot',
                     'ClusterPairsPlot',
                     'hgmmcpp'),
        'hgmmcmll' : ('HGMM Cluster Means Level Lines',
                      'ClusterMeansLevelLines',
                      'hgmmcmll'),
        'hgmmcmlh' : ('HGMM Cluster Means Level Heatmap',
                      'HierarchicalStackedClusterMeansHeatmap',
                      'hgmmcmlh')
    },
    'eeg' : {
    },
    'fmri' : {
    },
    'graph' : {
        'hgmmscmh' : ('HGMM Stacked Cluster Means Heatmap',
                      'ClusterMeansLevelHeatmap',
                      'hgmmscmh'),
        'hgmmcmd' : ('HGMM Cluster Means Dendrogram',
                     'HierarchicalClusterMeansDendrogram',
                     'hgmmcmd'),
        'hgmmcpp' : ('HGMM Pairs Plot',
                     'ClusterPairsPlot',
                     'hgmmcpp'),
        'hgmmcmll' : ('HGMM Cluster Means Level Lines',
                      'ClusterMeansLevelLines',
                      'hgmmcmll'),
        'hgmmcmlh' : ('HGMM Cluster Means Level Heatmap',
                      'HierarchicalStackedClusterMeansHeatmap',
                      'hgmmcmlh')
    }
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
    metadata = dict()
    if plot_name == "default":
        todisp = "<h1> Choose a plot! </h1>"
    elif subj_name == "none" and mode == 'one':
        ids = mongo_get.get_from_dataset(ds_name)
        subjs = mongo_get.get_from_database(ds_name, ids)
        print('Getting from db subjs', subjs)

        for id in ids:
            # TODO: How are we handling tasks
            tasks.append(['Rest'])
            # if modality == 'fmri':
            #     tasks.append([task_di for task_di in os.listdir(os.path.join(base_path, id, 'Nifti4DPlotter'))
            #                   if os.path.isdir(os.path.join(base_path, id, 'Nifti4DPlotter', task_di))])
        todisp = None
    elif plot_name is not None:
        # Rendering a plot
        dm_path = modality
        options = aggregate_options
        if mode == 'embed':
            dm_path += '_embed'
            options = embedded_options
        elif mode == 'one':
            options = one_to_one_options
            if modality == 'eeg' and 'spatial' in plot_name:
                dm_path += '_spatial'
        elif mode == 'clust':
            dm_path += '_clust'
            options = clustering_options
        dm_path += '_dm.pkl'

        if modality == 'eeg' and 'spatial' in plot_name:
            with open(os.path.join('data', ds_name, 'eeg_chanlocs.pkl'), 'rb') as chanloc_pkl, open(os.path.join('data', ds_name, dm_path), 'rb') as pkl_loc:
                DM = pkl.load(pkl_loc)
                chanlocs = pkl.load(chanloc_pkl)
                print(len(chanlocs))
                print(DM.D)
                todisp = getattr(lpl, options[modality][plot_name][1])(DM.getResourceDS(0), mode='div').plot(chanlocs)
        else:
            with open(os.path.join('data', ds_name, dm_path), 'rb') as pkl_loc:
                DM = pkl.load(pkl_loc)
                todisp = getattr(lpl, options[modality][plot_name][1])(DM, mode='div').plot()

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
        for title, _, tag in one_to_one_options[modality].values():
            if tag == plot_name: plot_title = title

    if len(subjs) > 0:
        metadata = subjs[0]['metadata']


    return render_template('meda_modality.html',
                           interm=zip(subjs, tasks),
                           interm_meta=metadata,
                           one_title=plot_title,
                           plot=todisp,
                           MEDA_options = aggregate_options[modality].values(),
                           MEDA_Embedded_options = embedded_options[modality].values(),
                           MEDA_Clustering_options = clustering_options[modality].values(),
                           One_to_One = one_to_one_options[modality].values(),
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

    file_names = ['pheno', 'eeg', 'fmri', 'graph']

    for name in file_names:
        files = request.files.getlist(name)
        # app.logger.info('Input type: %s, File name: %s', name, file.filename)
        if len(files) != 0 and files[0].filename != '':
            file = files[0]
            app.logger.info('Input type in loop: %s', name)
            dirpath = os.path.join(dspath, name)
#            os.makedirs(dirpath, exist_ok=True)
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
#
            # Collect AWS credentials,
            credential_info = open(session[name+'_data'], 'r').read().split(",")
            bucket_name = credential_info[0]
#            ACCESS_KEY = str(credential_info[1])
#            SECRET_KEY = str(credential_info[2])
#
#            # Download files
#            '''
#            s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-east-1')
#            bucket = s3.Bucket(bucket_name)
#            for elem in bucket.list():
#                key = elem.name.encode('utf-8')
#                bucket.download_file(key, os.path.join(session['basepath'], name)+"/"+str(key.split('/')[-1]))
#            '''
#

            try:
                print('About to try!')
                cmd = ["aws", "s3",
                       "cp", ("s3://%s/%s")%(bucket_name, name),
                       os.path.join(session['basepath'], name), "--recursive"]
                call(cmd)
                app.logger.info(name+" Data Downloaded")
            except:
                print("Download from S3 failed!")

            try:
                mongo_update.build_database(filedir, bucket_name)
            except:
                print("Database synchronization failed!")

            run_modality(name, os.path.basename(session['basepath']))

    # For modalities in which you upload the dataset itself.
    if session['pheno_data'] is not None:
        try:
            pheno.run_pheno(session['pheno_data'])
            mongo_update.build_metadata(session['pheno_data'], filedir)
        except:
            print("Running plots/synchronization failed!")

    for name in file_names:
        if session[name+'_data'] is not None:
            return redirect(url_for('meda_modality', ds_name=filedir, modality=name, mode='none', plot_name='default'))


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
