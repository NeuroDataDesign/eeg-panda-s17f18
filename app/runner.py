import os
import pandas as pd
import pickle as pkl

# Load the lemur library
import sys
sys.path.append("..")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.embedders as leb

def run_modality(name, modality):

    # Set root paths and parse data
    if modality == 'pheno':
        DATASET = os.path.split(os.path.split(name)[0])[1]
    else:
        BASE = "data"
        DATASET = "%s/%s"%(name, modality)
        root = os.path.join(BASE, DATASET)
        bp = lds.BIDSParser(root)

    # For each modality, set specific settings
    if modality == 'eeg':
        dataset_descriptor = bp.getModalityFrame("preprocessed", ".pkl").iloc[:6]
        DS = lds.EEGDataSet(dataset_descriptor)
        metric = lms.FroCorr
    elif modality == 'fmri':
        dataset_descriptor = bp.getmodalityframe("func", "nii.gz")
        DS = lds.fMRIDataSet(dataset_descriptor)
        metric = lms.DiffAve
    elif modality == 'graph':
        dataset_descriptor = bp.getModalityFrame("func", ".edgelist")
        DS = lds.GraphDataSet(dataset_descriptor)
        metric = lms.FroCorr
    else:
        raise ValueError('')

    with open(os.path.join(BASE, name, 'eeg_ds.pkl'), 'wb') as pkl_loc:
        pkl.dump(eds, pkl_loc)

    # Create a lemur distance matrix
    DM = lds.DistanceMatrix(DS, metric)
    DM.name = "eeg-DistanceMatrix"
    with open(os.path.join(BASE, name, 'eeg_dm.pkl'), 'wb') as pkl_loc:
        pkl.dump(DM, pkl_loc)

    # Create an embedded distance matrix object under MDS
    MDSEmbedder = leb.MDSEmbedder(num_components=10)
    EEG_Embedded = MDSEmbedder.embed(DM)
    with open(os.path.join(BASE, name, 'eeg_embed_dm.pkl'), 'wb') as pkl_loc:
        pkl.dump(EEG_Embedded, pkl_loc)


    chanlocs = pd.read_csv("data/%s/eeg/chanlocs.csv"%(name))
    with open(os.path.join(BASE, name, 'eeg_chanlocs.pkl'), 'wb') as pkl_loc:
        pkl.dump(chanlocs.as_matrix()[:, 1:4], pkl_loc)

    spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
    spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)
    with open(os.path.join(BASE, name, 'eeg_spatial_dm.pkl'), 'wb') as pkl_loc:
        pkl.dump(spatialDM, pkl_loc)

