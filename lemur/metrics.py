import numpy as np

class FroCorr:
        
    def parameterize(D):
        with np.errstate(divide = 'ignore', invalid = 'ignore'):
            return list(map(lambda j: np.nan_to_num(np.corrcoef(D.getResource(j))), range(D.N)))

    def compare(x, y):
        return np.linalg.norm(x - y)
