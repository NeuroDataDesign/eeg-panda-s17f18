import os
import pandas as pd
import numpy as np
import pickle as pkl

class DiskDataSet:

    def __init__(self, df_path):
        self.D = pd.read_csv(df_path)
        self.N = self.D.shape[0]
        self.name = df_path.split("/")[-1].split(".")[0].split("_")[0]

    def getResource(self, index):
        resource_path = self.D["resource_path"].ix[index]
        dim_column = self.D["dim_column"].ix[index]
        with open(resource_path, "rb") as f:
            if dim_column:
                return pkl.load(f).T
            return pkl.load(f)

class DistanceMatrix:

    def __init__(self, dataset, metric):
        self.dataset = dataset
        self.metric = metric
        self.N = self.dataset.N
        parameterization = self.metric.parameterize(self.dataset)
        self.matrix = np.zeros([self.N, self.N])
        for i in range(self.N):
            I = parameterization[i]
            for j in range(i + 1):
                J = parameterization[j]
                self.matrix[i, j] = self.metric.compare(I, J)
                self.matrix[j, i] = self.matrix[i, j]

    def getMatrix(self):
        return self.matrix
