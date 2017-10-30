import numpy as np
from numba import jit

class FroMetric:
    def __init__(self, dataset):
        self.correls = list(map(lambda x: x.dot(x.T) / x.shape[1] if x is not None else None, dataset))
        self.N = len(self.correls)
        self.n = self.correls[0].shape[0]
    
    def distance(self, i, j):
        if self.correls[i] is None or self.correls[j] is None:
            return np.nan
        else:
            return np.linalg.norm(self.correls[i] - self.correls[j]) / self.n**2

class ErosMetric:
    def __init__(self, dataset, agg):
        eigenvals, right_evs = self.eros_preprocess(dataset)
        self.right_evs = right_evs
        self.S = np.column_stack(eigenvals)
        self.N = self.S.shape[1]
        self.n = self.S.shape[0]
        self.w = self.compute_weight_ratio(self.S, agg)
        
    def get_evecs_evals(self, A):
        B = (A.T.dot(A)) / A.shape[0]
        _, D, E = np.linalg.svd(B, full_matrices=False)
        return D, E

    def eros_preprocess(self, dset):
        eigenvalues = []
        right_evs = []
        for A in dset:
            A = A - np.mean(A, axis=0)
            D, E = self.get_evecs_evals(A)
            eigenvalues.append(D)
            right_evs.append(E)
        return eigenvalues, right_evs
    
    def compute_weight_raw(self, S, fn):
        w = fn(S, axis=1)
        w_norm = w / np.sum(w)
        return w_norm
    
    def compute_weight_ratio(self, S, fn):
        column_sum = np.sum(S, axis=0)
        S_norm = np.divide(S, column_sum)
        return self.compute_weight_raw(S, fn)
    
    def distance(self, i, j):
        Av = self.right_evs[i]
        Bv = self.right_evs[j]
        s = 0.0
        for i in range(self.n):
            s += self.w[i] * np.abs(Av[:, i].T.dot(Bv[:, i]))
        # Hacky way to get rid of numerical error
        if 2.0 - 2 * s < 1e-10:
            s = 1.0
        return np.sqrt(2.0 - 2 * s) / np.sqrt(2)

def getDistMat(Metric):
    N = Metric.N
    dist_mat = np.zeros([N, N])
    for i in range(N):
        for j in range(N):
            dist_mat[i, j] = Metric.distance(i, j)
            dist_mat[j, i] = dist_mat[i, j] 
    return dist_mat

def getLabels(labels, N):
    per = N // len(labels)
    axislabels = [""] * N
    for i in range(len(labels)):
        start = per // 2
        axislabels[start + per * i] = labels[i]
    return axislabels

def distMatInnerOuter(distMat, labels):
    inner = []
    outer = []
    n = distMat.shape[0]
    for i in range(n):
        for j in range(i + 1):
            if labels[i] == labels[j]:
                if i != j:
                    inner.append(distMat[i, j])
            else:
                outer.append(distMat[i, j])
    return inner, outer


@jit(nopython=True,  cache=True)
def energy_distance(x, y):
    n = len(x)
    sxy = 0
    sxx = 0
    syy = 0
    for i in range(n):
        for j in range(i + 1):
            sxy += np.abs(x[i] - y[j])
            sxx += np.abs(x[i] - x[j])
            syy += np.abs(y[i] - y[j])
    return 2 * 2 * sxy / (n*n) - 2 * sxx / (n*n) - 2 * syy / (n*n)
