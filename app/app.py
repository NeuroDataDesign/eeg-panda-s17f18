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

import pheno
from runner import run_modality

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
        'connectedscatter': ('Connected Scatter', 'ConnectedScatterplot', 'connectedscatter'),
        'sparkline': ('Sparkline', 'SparkLinePlotter', 'sparkline'),
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


    subjs = []
    tasks = []
    metadata = dict()

    plot_title = ""
    if mode == "one":
        for title, _, tag in one_to_one_options[modality].values():
            if tag == plot_name: plot_title = title

    try:
        datatype = request.args.get('datatype')
    except:
        datatype = 'func'

    print(datatype)
    datatype = 'func'

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
        dm_dir = os.path.join('data', ds_name, modality, datatype)
        dm_path = ''
        # Choose options
        options = aggregate_options
        if mode == 'embed':
            options = embedded_options
        elif mode == 'one':
            options = one_to_one_options
        elif mode == 'clust':
            options = clustering_options

        # Choose filepath
        if mode == 'embed' or mode == 'cluster':
            dm_path += 'embed_'

        if mode == 'one':
            dm_path += 'ds.pkl'
        else:
            dm_path += 'dm.pkl'

        # Actually set to disp
        with open(os.path.join(dm_dir, dm_path), 'rb') as dm_loc:
            DM = pkl.load(dm_loc)
            if mode == 'one':
                if modality == 'eeg' and 'spatial' in plot_name:
                    with open(os.path.join('data', ds_name, 'eeg', 'chanlocs.pkl'), 'rb') as chanloc_pkl:
                        chanlocs = pkl.load(chanloc_pkl)
                        todisp = getattr(lpl, options[modality][plot_name][1])(DM.getResourceDS(0), mode='div').plot(chanlocs)
                elif modality == 'eeg' and 'connectedscatter' in plot_name:
                    with open(os.path.join('data', ds_name, 'eeg', 'spatial_dm.pkl'), 'rb') as spatial_pkl:
                        spatial = pkl.load(spatial_pkl)
                        todisp = getattr(lpl, options[modality][plot_name][1])(DM.getResourceDS(0), mode='div').plot(spatial)
                elif modality == 'eeg' and 'sparkline' in plot_name:
                    todisp = getattr(lpl, options[modality][plot_name][1])(DM.getResourceDS(0), mode='div').plot(sample_freq=500)
                else:
                    todisp = getattr(lpl, options[modality][plot_name][1])(DM.getResourceDS(0), mode='div').plot()

            else:
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


@app.route('/upload', methods=['POST'])
def upload():

    target = os.path.join(APP_ROOT,'data')
    app.logger.info('Target route: %s', target)

    filedir = request.form['dataset-name']
    dspath = os.path.join(target, filedir)
    os.makedirs(dspath, exist_ok=True)
    session['basepath'] = dspath


    ########################################
    # Other Modalities

    # For modalities in which you upload S3 credentials.
    for name in ['eeg', 'fmri', 'graph']:
        bucket_name = request.form[name]
        bucket_key = request.form[name+'-key']
        session[name] = True
        if bucket_name is None or len(bucket_name) == 0:
            session[name] = False
            continue

        # Make folders to load files into
        dirpath = os.path.join(dspath, name)
        os.makedirs(dirpath, exist_ok=True)

        # Download patients
        app.logger.info("Downloading "+name+" Data...")
        # Download files
        try:
            cmd = ["aws", "s3",
                   "cp", ("s3://%s/%s")%(bucket_name, bucket_key),
                   os.path.join(session['basepath'], name), "--recursive"]
            call(cmd)
            app.logger.info(name+" Data Downloaded")
        except:
            print("Download from S3 failed!")

        bp, modality_list = run_modality(os.path.basename(session['basepath']), name)
        print(bp)

        try:
            mongo_update.build_database(filedir, bp, modality_list)
        except:
            print("Database synchronization failed!")


    ########################################
    # Phenotypic

    files = request.files.getlist('pheno')
    # Check if phenotypic files have been uploaded
    session['pheno'] = False
    if len(files) != 0 and files[0].filename != '':
        session['pheno'] = True

        # Upload the file
        file = files[0]
        app.logger.info('Uploading Phenotypic Data')
        dirpath = os.path.join(dspath, 'pheno')
        os.makedirs(dirpath, exist_ok=True)
        filename = file.filename
        destination = os.path.join(dspath, filename)
        app.logger.info('Accept incoming file: %s', filename)
        app.logger.info('Save it to: %s', destination)
        file.save(destination)

        try:
            pheno.run_pheno(destination)
            mongo_update.build_metadata(destination, filedir)
        except:
            print("Running plots/synchronization failed!")

    for name in ['pheno', 'eeg', 'fmri', 'graph']:
        if session[name]:
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
