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


  chanlocs = pd.read_csv("data/%s/eeg/chanlocs.csv"%(name))
  with open(os.path.join(BASE, name, 'eeg_chanlocs.pkl'), 'wb') as pkl_loc:
      pkl.dump(chanlocs.as_matrix()[:, 1:4], pkl_loc)
  
  spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
  spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)
  with open(os.path.join(BASE, name, 'eeg_spatial_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(spatialDM, pkl_loc)


  # TODO: Yujia no idea what's happneing here...
  # s3 = boto3.resource('s3')
  # bucket = s3.Bucket('redlemurtest')
  #     # Directly read through S3 bucket and pass into pandas dataframe
  # for obj in bucket.objects.all():
  #     key = obj.key
  #     if key.endswith('chanlocs.csv'):
  #         body = obj.get()['Body'].read()
  #         chanlocs = pd.read_csv(io.BytesIO(body))
  # spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
  # spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)
#  chanlocs = pd.read_csv("data/%s/eeg/chanlocs.csv"%(name))
#  spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
#  spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)
