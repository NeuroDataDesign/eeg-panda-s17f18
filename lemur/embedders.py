from sklearn.manifold import TSNE, MDS

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
