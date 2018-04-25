
# coding: utf-8

# In[1]:


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
#  DATASET = "%s/eeg"%(name)
#  root = os.path.join(BASE, DATASET)
  bp = lds.BIDSParser()
  dataset_descriptor = bp.getModalityFrame("preprocessed", ".pkl").iloc[:6]
  print(dataset_descriptor)
  out_base = os.path.join(BASE, name, "eeg_derivatives")
  out_emb_base = os.path.join(BASE, name, "eeg_embedded_deriatives")
  os.makedirs(out_base + "/agg", exist_ok=True)
  os.makedirs(out_emb_base + "/agg", exist_ok=True)


  # In[2]:


  eds = lds.EEGDataSet(dataset_descriptor)
  # Create a lemur distance matrix based on the EEG data
  DM = lds.DistanceMatrix(eds, lms.FroCorr)
  DM.name = "eeg-DistanceMatrix"

  with open(os.path.join(BASE, name, 'eeg_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(DM, pkl_loc)



  # In[3]:


  # Create an embedded distance matrix object under MDS
  MDSEmbedder = leb.MDSEmbedder(num_components=10)
  EEG_Embedded = MDSEmbedder.embed(DM)


  # In[4]:
  s3 = boto3.resource('s3')
  bucket = s3.Bucket('redlemurtest')
      # Directly read through S3 bucket and pass into pandas dataframe
  for obj in bucket.objects.all():
      key = obj.key
      if key.endswith('chanlocs.csv'):
          body = obj.get()['Body'].read()
          chanlocs = pd.read_csv(io.BytesIO(body))
  spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
  spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)
#  chanlocs = pd.read_csv("data/%s/eeg/chanlocs.csv"%(name))
#  spatial = lds.DataSet(chanlocs[["X", "Y", "Z"]], "Spatial")
#  spatialDM = lds.DistanceMatrix(spatial, lms.VectorDifferenceNorm)


  # In[5]:


  for i in range(eds.n):
      print(i)
      single_ds = eds.getResourceDS(i)
      lpl.SparkLinePlotter(single_ds, mode="savediv",
                           base_path=out_base).plot(sample_freq=500)


  # In[6]:

  # Get 3D locations
  locs = chanlocs.as_matrix()[:, 1:4]
  for i in range(eds.n):
      lpl.SpatialTimeSeries(eds.getResourceDS(i), mode="savediv", base_path=out_base).plot(locs)
      lpl.SpatialPeriodogram(eds.getResourceDS(i), mode="savediv", base_path=out_base).plot(locs)


  # In[7]:


  for i in range(eds.n):
      print(i)
      single_ds = eds.getResourceDS(i)
      single_DM = lds.DataSet(single_ds.D.corr(), single_ds.name)
      lpl.ConnectedScatterplot(single_DM,
                               mode="savediv",
                               base_path=out_base).plot(spatialDM)


  # In[1]:


  lpl.SquareHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.Heatmap(EEG_Embedded, mode="savediv", base_path=out_emb_base).plot()


  # In[9]:


  lpl.EigenvectorHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.EigenvectorHeatmap(EEG_Embedded, mode="savediv",
                         base_path=out_emb_base).plot()


  # In[10]:


  lpl.LocationHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.LocationHeatmap(EEG_Embedded, mode="savediv",
                      base_path=out_emb_base).plot()


  # In[11]:


  lpl.LocationLines(DM, mode="savediv", base_path=out_base).plot()
  lpl.LocationLines(EEG_Embedded, mode="savediv",
                    base_path=out_emb_base).plot()


  # In[12]:


  lpl.HistogramHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.HistogramHeatmap(EEG_Embedded, mode="savediv",
                       base_path=out_emb_base).plot()


  # In[13]:


  lpl.CorrelationMatrix(DM, mode="savediv",
                        base_path=out_base).plot()
  lpl.CorrelationMatrix(EEG_Embedded, mode="savediv",
                        base_path=out_emb_base).plot()


  # In[14]:


  lpl.ScreePlotter(DM, mode="savediv",
                   base_path=out_base).plot()
  lpl.ScreePlotter(EEG_Embedded, mode="savediv",
                   base_path=out_emb_base).plot()


  # In[15]:


  #lpl.HGMMClusterMeansDendrogram(DM, mode="savediv",
  #                               base_path=out_base).plot(level=1)
  #lpl.HGMMClusterMeansDendrogram(EEG_Embedded, mode="savediv",
  #                               base_path=out_emb_base).plot(level=1)


  # In[16]:


  #lpl.HGMMStackedClusterMeansHeatmap(DM, mode="savediv",
  #                                   base_path=out_base).plot(level=1)
  #lpl.HGMMStackedClusterMeansHeatmap(EEG_Embedded, mode="savediv",
  #                                   base_path=out_emb_base).plot(level=1)


  # In[17]:


  #lpl.HGMMClusterMeansLevelLines(DM, mode="savediv",
  #                               base_path=out_base).plot(level=1)
  #lpl.HGMMClusterMeansLevelLines(EEG_Embedded, mode="savediv",
  #                               base_path=out_emb_base).plot(level=1)


  # In[18]:


  lpl.ScreePlotter(DM, mode="savediv", base_path=out_base).plot()
  lpl.ScreePlotter(EEG_Embedded, mode="savediv",
                   base_path=out_emb_base).plot()
