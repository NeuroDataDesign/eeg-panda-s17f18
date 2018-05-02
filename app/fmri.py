
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
  bp = lds.BIDSParser(root)
  dataset_descriptor = bp.getModalityFrame("func", "nii.gz")
  # out_base = os.path.join(BASE, name, "fmri_derivatives")
  # out_emb_base = os.path.join(BASE, name, "fmri_embedded_deriatives")
  # os.makedirs(out_base + "/agg", exist_ok=True)
  # os.makedirs(out_emb_base + "/agg", exist_ok=True)

  fds = lds.fMRIDataSet(dataset_descriptor)
  # Create a lemur distance matrix based on the EEG data
  DM = lds.DistanceMatrix(fds, lms.DiffAve)
  DM.name = "fmri-DistanceMatrix"
  with open(os.path.join(BASE, name, 'fmri_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(DM, pkl_loc)


  # Create an embedded distance matrix object under MDS
  MDSEmbedder = leb.MDSEmbedder(num_components=10)
  fMRI_Embedded = MDSEmbedder.embed(DM)
  with open(os.path.join(BASE, name, 'fmri_embed_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(fMRI_Embedded, pkl_loc)
