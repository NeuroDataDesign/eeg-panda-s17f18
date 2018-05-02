
# coding: utf-8

# In[1]:


import os
import pickle as pkl

# Load the lemur library
import sys
sys.path.append("..")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.plotters as lpl
import lemur.embedders as leb


def run_fmri(name):
  BASE = "data"
  DATASET = "%s/fmri"%(name)
  root = os.path.join(BASE, DATASET)
  print(root)
  bp = lds.BIDSParser(root)
  dataset_descriptor = bp.getModalityFrame("func", "nii.gz")
  print(dataset_descriptor)
  out_base = os.path.join(BASE, name, "fmri_derivatives")
  out_emb_base = os.path.join(BASE, name, "fmri_embedded_deriatives")
  os.makedirs(out_base + "/agg", exist_ok=True)
  os.makedirs(out_emb_base + "/agg", exist_ok=True)


  # In[2]:


  fds = lds.fMRIDataSet(dataset_descriptor)
  # Create a lemur distance matrix based on the EEG data
  DM = lds.DistanceMatrix(fds, lms.DiffAve)
  DM.name = "fmri-DistanceMatrix"
  with open(os.path.join(BASE, name, 'fmri_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(DM, pkl_loc)


  # In[4]:


  # Create an embedded distance matrix object under MDS
  MDSEmbedder = leb.MDSEmbedder(num_components=10)
  fMRI_Embedded = MDSEmbedder.embed(DM)
  with open(os.path.join(BASE, name, 'fmri_embed_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(fMRI_Embedded, pkl_loc)


  # In[17]:

  '''
  for i in range(fds.n):
      lpl.Nifti4DPlotter(fds.getResource(i)).plot(downsample=5,
      out_base=out_base)
  '''


  # In[5]:


  lpl.SquareHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.SquareHeatmap(fMRI_Embedded, mode="savediv",
                    base_path=out_emb_base).plot()


  # In[6]:


  lpl.EigenvectorHeatmap(DM, mode="savediv",
                         base_path=out_base).plot()
  lpl.EigenvectorHeatmap(fMRI_Embedded, mode="savediv",
                         base_path=out_emb_base).plot()


  # In[7]:


  lpl.LocationHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.LocationHeatmap(fMRI_Embedded, mode="savediv",
                      base_path=out_emb_base).plot()


  # In[8]:


  lpl.LocationLines(DM, mode="savediv", base_path=out_base).plot()
  lpl.LocationLines(fMRI_Embedded, mode="savediv",
                    base_path=out_emb_base).plot()


  # In[9]:


  lpl.HistogramHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.HistogramHeatmap(fMRI_Embedded, mode="savediv",
                       base_path=out_emb_base).plot()


  # In[10]:


  lpl.CorrelationMatrix(DM, mode="savediv",
                        base_path=out_base).plot()
  lpl.CorrelationMatrix(fMRI_Embedded, mode="savediv",
                        base_path=out_emb_base).plot()


  # In[11]:


  lpl.ScreePlotter(DM, mode="savediv", base_path=out_base).plot()
  lpl.ScreePlotter(fMRI_Embedded, mode="savediv",
                   base_path=out_emb_base).plot()


  # In[12]:


  #lpl.HGMMClusterMeansDendrogram(DM,mode="savediv", base_path=out_base).plot(level=1)
  #lpl.HGMMClusterMeansDendrogram(fMRI_Embedded,
  #                               mode="savediv",
  #                               base_path=out_emb_base).plot(level=1)


  # In[13]:


  #lpl.HGMMStackedClusterMeansHeatmap(DM,mode="savediv", base_path=out_base).plot(level=2)
  #lpl.HGMMStackedClusterMeansHeatmap(fMRI_Embedded,
  #                                   mode="savediv",
  #                                   base_path=out_emb_base).plot(level=2)


  # In[14]:


  #lpl.HGMMClusterMeansLevelLines(DM,mode="savediv", base_path=out_base).plot(level=2)
  #lpl.HGMMClusterMeansLevelLines(fMRI_Embedded,
  #                               mode="savediv",
  #                               base_path=out_emb_base).plot(level=2)
