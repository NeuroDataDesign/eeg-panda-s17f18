# coding: utf-8
import os
import pandas as pd
import sys
import pickle as pkl


# Load the lemur library
import sys
sys.path.append("..")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.plotters as lpl
import lemur.embedders as leb
import lemur.clustering as lcl

def run_graph(name):
  BASE = "data"
  DATASET = "%s/graph"%(name)
  root = os.path.join(BASE, DATASET)
  bp = lds.BIDSParser(root)
  dataset_descriptor = bp.getModalityFrame("func", ".edgelist")

  gds = lds.GraphDataSet(dataset_descriptor)
  # Create a lemur distance matrix based on the graph data
  DM = lds.DistanceMatrix(gds, lms.FroCorr)
  DM.name = "graph-DistanceMatrix"
  with open(os.path.join(BASE, name, 'graph_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(DM, pkl_loc)

  # Create an embedded distance matrix object under MDS
  MDSEmbedder = leb.MDSEmbedder(num_components=10)
  Graph_Embedded = MDSEmbedder.embed(DM)
  with open(os.path.join(BASE, name, 'graph_embed_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(Graph_Embedded, pkl_loc)

  ##### Clustering
  Graph_Embedded = lcl.HGMMClustering(Graph_Embedded, 4)
  Graph_Embedded.cluster()
  with open(os.path.join(BASE, name, 'graph_clust_dm.pkl'), 'wb') as pkl_loc:
      pkl.dump(Graph_Embedded, pkl_loc)
