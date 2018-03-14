# coding: utf-8

# In[1]:


import os
import pandas as pd
import sys


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
  print(dataset_descriptor)
  out_base = os.path.join(BASE, name, "graph_derivatives")
  out_emb_base = os.path.join(BASE, name, "graph_embedded_deriatives")
  os.makedirs(out_base + "/agg", exist_ok=True)
  os.makedirs(out_emb_base + "/agg", exist_ok=True)

  gds = lds.GraphDataSet(dataset_descriptor)
  print(gds.n)
  print(gds.D["subjects"].astype(str))
  # Create a lemur distance matrix based on the graph data
  DM = lds.DistanceMatrix(gds, lms.FroCorr)
  DM.name = "graph-DistanceMatrix"

  # Create an embedded distance matrix object under MDS
  MDSEmbedder = leb.MDSEmbedder(num_components=10)
  Graph_Embedded = MDSEmbedder.embed(DM)

# In[1]:


  lpl.SquareHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.Heatmap(Graph_Embedded, mode="savediv", base_path=out_emb_base).plot()
  # In[9]:


  lpl.EigenvectorHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.EigenvectorHeatmap(Graph_Embedded, mode="savediv",
                       base_path=out_emb_base).plot()


    # In[10]:


  lpl.LocationHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.LocationHeatmap(Graph_Embedded, mode="savediv",
                    base_path=out_emb_base).plot()


    # In[11]:


  lpl.LocationLines(DM, mode="savediv", base_path=out_base).plot()
  lpl.LocationLines(Graph_Embedded, mode="savediv",
                  base_path=out_emb_base).plot()


    # In[12]:


  lpl.HistogramHeatmap(DM, mode="savediv", base_path=out_base).plot()
  lpl.HistogramHeatmap(Graph_Embedded, mode="savediv",
                     base_path=out_emb_base).plot()


    # In[13]:


  lpl.CorrelationMatrix(DM, mode="savediv",
                      base_path=out_base).plot()
  lpl.CorrelationMatrix(Graph_Embedded, mode="savediv",
                      base_path=out_emb_base).plot()


    # In[14]:


  lpl.ScreePlotter(DM, mode="savediv",
                 base_path=out_base).plot()
  lpl.ScreePlotter(Graph_Embedded, mode="savediv",
                 base_path=out_emb_base).plot()


  ##### Clustering
  hgmm = lcl.HGMMClustering(Graph_Embedded, 4)
  try:
      hgmm.cluster()

      # In[ ]:


      lpl.ClusterPairsPlot(hgmm, mode="savediv", base_path=out_emb_base).plot()


      # In[ ]:


      lpl.HierarchicalClusterMeansDendrogram(hgmm, mode="savediv", base_path=out_emb_base).plot()


      # In[ ]:


      lpl.HierarchicalStackedClusterMeansHeatmap(hgmm, mode="savediv", base_path=out_emb_base).plot()


      # In[ ]:


      lpl.ClusterMeansLevelHeatmap(hgmm, mode="savediv", base_path=out_emb_base).plot()


      # In[ ]:


      lpl.ClusterMeansLevelLines(hgmm, mode="savediv", base_path=out_emb_base).plot()
  except:
      print("Number components was greater than number of data points.")

  lpl.GraphPlotter(gds, base_path=out_base).makeplot(modality='func')
