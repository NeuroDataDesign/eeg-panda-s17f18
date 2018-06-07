import os
import pandas as pd
import pickle as pkl
import boto3
import io
import glob

# Load the lemur library
import sys
sys.path.append("..")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.plotters as lpl
import lemur.clustering as lcl
import lemur.embedders as leb

def run_eeg(name):
  BASE = "data"
  DATASET = "%s/eeg"%(name)
  root = os.path.join(BASE, DATASET)
  bp = lds.BIDSParser(root)
  dataset_descriptor = bp.getModalityFrame("preprocessed", ".pkl").iloc[:6]
  # out_base = os.path.join(BASE, name, "eeg_derivatives")
  # out_emb_base = os.path.join(BASE, name, "eeg_embedded_deriatives")
  # os.makedirs(out_base + "/agg", exist_ok=True)
  # os.makedirs(out_emb_base + "/agg", exist_ok=True)

  eds = lds.EEGDataSet(dataset_descriptor)
  with open(os.path.join(BASE, name, 'eeg_ds.pkl'), 'wb') as pkl_loc:
      pkl.dump(eds, pkl_loc)

  # Create a lemur distance matrix based on the EEG data
  DM = lds.DistanceMatrix(eds, lms.FroCorr)
  DM.name = "eeg-DistanceMatrix"
  with open(os.path.join(BASE, name, 'eeg_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(DM, pkl_loc)

  # Create an embedded distance matrix object under MDS
  MDSEmbedder = leb.MDSEmbedder(num_components=10)
  EEG_Embedded = MDSEmbedder.embed(DM)
  with open(os.path.join(BASE, name, 'eeg_embed_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(EEG_Embedded, pkl_loc)

  hgmm = lcl.HGMMClustering(EEG_Embedded, 4)
  hgmm.cluster()
  with open(os.path.join(root, 'hgmm_clust_dm.pkl'), 'wb') as pkl_loc:
    pkl.dump(hgmm, pkl_loc)

  clustered = lcl.AdaptiveKMeans(EEG_Embedded)
  clustered.cluster()
  with open(os.path.join(root, 'km_clust_dm.pkl'), 'wb') as pkl_loc:
    pkl.dump(clustered, pkl_loc)

  chanlocs = pd.read_csv("data/%s/eeg/chanlocs.csv"%(name))
  with open(os.path.join(BASE, name, 'eeg_chanlocs.pkl'), 'wb') as pkl_loc:
      pkl.dump(chanlocs.as_matrix()[:, 1:4], pkl_loc)
  
  spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
  spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)
  with open(os.path.join(BASE, name, 'eeg_spatial_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(spatialDM, pkl_loc)

