from sklearn.manifold import TSNE, MDS
import numpy as np

class BaseEmbedder:
    def __init__(self, num_components = 2):
        self.num_components = num_components

class MDSEmbedder(BaseEmbedder):
    embedding_name = "MDS"
    def embed(self, M):
        mds = MDS(n_components = self.num_components, dissimilarity="precomputed")
        mds.fit(M)
        emb = mds.embedding_
        return emb

class TSNEEmbedder(BaseEmbedder):
    embedding_name = "TSNE"
    def embed(self, M):
        tsne = TSNE(n_components = self.num_components, metric="precomputed")
        tsne.fit(M)
        emb = tsne.embedding_
        return emb 

def PCA(D):
    d, n = D.shape
    mu = np.mean(D, axis=1).reshape(d, 1)
    D = D - mu
    U, s, Vt = np.linalg.svd(D, full_matrices=False)
    return U, s, Vt, mu

class PCAEmbedder(BaseEmbedder):
    embedding_name = "PCA"
    def embed(self, M):
        U, s, Vt, m = PCA(M) 
        return (U[:, :self.num_components].T.dot(M)).T  
