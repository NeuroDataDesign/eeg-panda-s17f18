
# coding: utf-8

# In[ ]:


# Outside imports
import pandas as pd
import numpy as np
import os


# In[ ]:


# Load the lemur library
import sys
sys.path.append(".")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.plotters as lpl
import lemur.clustering as lcl
import lemur.embedders as leb

def run_pheno(name):

    # Create a lemur dataset based on the phenotypic data
    DATASET = os.path.split(os.path.split(name)[0])[1]
    CDS = lds.CSVDataSet(name, name = DATASET)
    metadata = CDS.saveMetaData(os.path.join("data", DATASET, "metadata.json"))
    CDS.imputeColumns("mean")
    DM = lds.DistanceMatrix(CDS, lms.VectorDifferenceNorm)

    # Create an embedded distance matrix object under MDS
    MDSEmbedder = leb.MDSEmbedder(num_components=10)
    HBN_Embedded = MDSEmbedder.embed(DM)

    # Set output paths for saved plots.
    BASE = "data"
    out_base = os.path.join(BASE, DATASET, "pheno_derivatives")
    out_emb_base = os.path.join(BASE, DATASET, "pheno_embedded_deriatives")
    os.makedirs(out_base + "/agg", exist_ok=True)
    os.makedirs(out_emb_base + "/agg", exist_ok=True)



    # In[ ]:


    lpl.Heatmap(CDS, mode="savediv", base_path=out_base).plot()
    lpl.Heatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()

    # In[ ]:


    lpl.LocationLines(CDS, mode="savediv", base_path = out_base).plot()
    lpl.LocationLines(HBN_Embedded, mode="savediv", base_path = out_emb_base).plot()

    # In[ ]:


    lpl.LocationHeatmap(CDS, mode="savediv", base_path=out_base).plot()
    lpl.LocationHeatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()

    # In[ ]:


    lpl.HistogramHeatmap(CDS, mode="savediv", base_path=out_base).plot()
    lpl.HistogramHeatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()


    # In[ ]:


    #lpl.CorrelationMatrix(CDS).plot()
    #lpl.CorrelationMatrix(HBN_Embedded).plot()
    #lpl.CorrelationMatrix(CDS, mode="savediv", base_path=out_base).plot()
    #lpl.CorrelationMatrix(HBN_Embedded, mode="savediv", base_path=out_base).plot()


    # In[ ]:


    lpl.ScreePlotter(CDS, mode="savediv", base_path=out_base).plot()
    lpl.ScreePlotter(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()


    # In[ ]:


    lpl.EigenvectorHeatmap(CDS, mode="savediv", base_path=out_base).plot()
    lpl.EigenvectorHeatmap(HBN_Embedded, mode="savediv", base_path=out_base).plot()


    ##### Clustering
    hgmm = lcl.HGMMClustering(HBN_Embedded, 4)
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
