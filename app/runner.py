import os
import pandas as pd
import pickle as pkl

# Load the lemur library
import sys
sys.path.append("..")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.embedders as leb
import lemur.clustering as lcl
import copy

def run_modality(name, modality):

    # Set root paths and parse data
    BASE = 'data'

    DATASET = '%s/%s'%(name, modality)
    root = os.path.join(BASE, DATASET)
    bp = lds.BIDSParser(root)

    # For each modality, set specific settings
    if modality == 'eeg':
        modality_list = [('preprocessed', '.pkl')]
        DS_type = lds.EEGDataSet
        metric = lms.FroCorr
    elif modality == 'fmri':
        modality_list = [
            ('func', 'nii.gz')
        ]
        DS_type = lds.fMRIDataSet
        metric = lms.DiffAve
    elif modality == 'graph':
        modality_list = [
            ('func', '.edgelist')
        ]
        DS_type = lds.GraphDataSet
        metric = lms.FroCorr
    else:
        raise ValueError('Needs to be eeg, fmri, or graph')

    # If EEG, save important metadata pkls
    if modality == 'eeg':
        chanlocs = pd.read_csv("data/%s/eeg/chanlocs.csv"%(name))
        with open(os.path.join("data/%s/eeg"%(name), 'chanlocs.pkl'), 'wb') as pkl_loc:
            pkl.dump(chanlocs.as_matrix()[:, 1:4], pkl_loc)

        spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
        spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)
        with open(os.path.join("data/%s/eeg"%(name), 'spatial_dm.pkl'), 'wb') as pkl_loc:
            pkl.dump(spatialDM, pkl_loc)

    # Iterate through potential files
    for datatype, f_ext in modality_list:

        dataset_descriptor = bp.getModalityFrame(datatype, f_ext)
        DS = DS_type(dataset_descriptor)
        print (DS)
        curr_dir = os.path.join(root, datatype)
        if os.path.exists(curr_dir):
            continue
        else:
            os.makedirs(curr_dir)

        # Save the dataset
        with open(os.path.join(curr_dir, 'ds.pkl'), 'wb') as pkl_loc:
            pkl.dump(DS, pkl_loc)

        # Create a lemur distance matrix
        if modality == 'fmri':
            DM = lds.DistanceMatrix(DS, metric, True)
        else:
            DM = lds.DistanceMatrix(DS, metric)
        DM.name = "%s-DistanceMatrix"%(modality)
        with open(os.path.join(curr_dir, 'dm.pkl'), 'wb') as pkl_loc:
            pkl.dump(DM, pkl_loc)

        # Create an embedded distance matrix object under MDS
        MDSEmbedder = leb.MDSEmbedder(num_components=10)
        embedded = MDSEmbedder.embed(DM)
        with open(os.path.join(curr_dir, 'embed_dm.pkl'), 'wb') as pkl_loc:
            pkl.dump(embedded, pkl_loc)

        ##### Clustering

        if DS.n > 10:
            clustered = lcl.HGMMClustering(embedded, 4)
            clustered.cluster()
            with open(os.path.join(curr_dir, 'hgmm_clust_dm.pkl'), 'wb') as pkl_loc:
                pkl.dump(clustered, pkl_loc)

            clustered = lcl.AdaptiveKMeans(embedded)
            clustered.cluster()
            with open(os.path.join(curr_dir, 'km_clust_dm.pkl'), 'wb') as pkl_loc:
                pkl.dump(clustered, pkl_loc)


    # Return modality list
    return bp, modality_list
