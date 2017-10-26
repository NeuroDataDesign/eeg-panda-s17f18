import numpy as np

def PCA(D):
    d, n = D.shape
    mu = np.mean(D, axis=1).reshape(d, 1)
    D = D - mu
    U, s, Vt = np.linalg.svd(D, full_matrices=False)
    return U, s, Vt, mu
    
