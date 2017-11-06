import numpy as np

class FroCorr:
    """An implementation the Frobenius-norm-of-correlation-matricies metric.

    This is not a class to be instantiated, but rather a way to organize and separate the 
    parameterization and comparison steps of the metric calculation to optimize a distance 
    matrix computation (e.g., compute the correlation matrix for each datapoint `once`, then
    just compare correlation matricies.

    """
        
    def parameterize(D):
        """Compute the correlation matrix of a single data point.

        Parameters
        ----------
        D : :obj:`DataSet`
            The lemur data set object to parameterize.

        Returns
        -------
        :obj:`list` of :obj:`ndarray`
            The correlation matrix of each object in the dataset.

        """
        with np.errstate(divide = 'ignore', invalid = 'ignore'):
            return list(map(lambda j: np.nan_to_num(np.corrcoef(D.getResource(j))), range(D.N)))

    def compare(x, y):
        """Compute the euclidian distance of two correlation matricies.

        Parameters
        ----------
        x : :obj:`ndarray`
            The left correlation matrix argument.
        y : :obj:`ndarray`
            The left correlation matrix argument.

        Returns
        -------
        float
            The distance.

        """
        return np.linalg.norm(x - y)

class NanDotProduct:
    """The dot product between two vectors, except nans are just treated as 0.

    """
        
    def parameterize(D):
        """Identity function.

        Parameters
        ----------
        D : :obj:`DataSet`
            A dataset.

        Returns
        -------
        :obj:`list` of :obj:`ndarray`
            The a list of each vector in the dataset.

        """

        return list(map(lambda j: D.getResource(j), range(D.N)))

    def compare(x, y):
        """Compute the euclidian distance of two correlation matricies.

        Parameters
        ----------
        x : :obj:`ndarray`
            The left vector argument.
        y : :obj:`ndarray`
            The left vector argument.

        Returns
        -------
        float
            The distance.

        """
        return np.nansum(x * y)
