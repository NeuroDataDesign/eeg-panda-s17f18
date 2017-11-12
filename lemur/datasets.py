import os
import pandas as pd
import numpy as np
import pickle as pkl

class DiskDataSet:
    """A dataset living locally on the hard disk.

    A disk data set is defined by a `.csv` file where entries of the `resource_path` column 
    are paths to local `.pkl` files, and all other columns describe variables of the data point 
    linked to by the `resource_path` variable. 

    Parameters
    ----------
    df_path : str
	Path to the .csv file describing the DiskDataSet.

    Attributes
    ----------
    D : pandas DataFrame
        A DataFrame object describing the dataset.
    N : int
        The number of observations in the dataset.
    name : string
        A descriptive name for the dataset.

    """

    def __init__(self, df_path):
        self.D = pd.read_csv(df_path)
        self.N = self.D.shape[0]
        self.name = df_path.split("/")[-1].split(".")[0].split("_")[0]

    def getResource(self, index):
        """Get a specific data point from the data set.

        Parameters
        ----------
        index : int
            The index of the data point in `D`.

        Returns
        -------
        :obj:`ndarray`
            A ndarray of the data point.

        """
        resource_path = self.D["resource_path"].ix[index]
        dim_column = self.D["dim_column"].ix[index]
        with open(resource_path, "rb") as f:
            if dim_column:
                return pkl.load(f).T
            return pkl.load(f)

def convertDtype(l):
    try:
        return np.array(l, dtype="float")
    except:
        pass
    l = np.array(l, dtype=str)
    l[l == 'nan'] = 'NA'
    return l

class CSVDataSet:
    """ A dataset living locally in a .csv file

    """
    def __init__(self, csv_path, index_column = None, column_level_names = None,
                 heirarchy_separator = ",", NA_val = "."):
        # Load the data set
        D = pd.read_csv(csv_path, dtype="unicode")

        # Set the index column as specified
        if index_column is not None:
            D[index_column] = list(map(str, D[index_column]))
            D.index = D[index_column]
            del D[index_column]

        # Set the column multi index
        column_tuples = list(map(lambda x: tuple(x.split(heirarchy_separator)), D.columns))
        D.columns = pd.MultiIndex.from_tuples(column_tuples)
        if column_level_names is not None:
            D.columns.names = column_level_names

        # Convert to numeric all numeric rows
        D = D.replace(NA_val, "nan")
        d = list(map(lambda c: convertDtype(list(D[c])), D.columns))
        newcolumns = D.columns
        newindex = D.index
        D = list(d)
        D = pd.DataFrame(dict(zip(newcolumns, D)), index = newindex)
        self.D = D

    def getResource(self, index):
        """Get a specific data point from the data set.

        Parameters
        ----------
        index : int or string
            The index of the data point in `D`, either positional or a string.

        Returns
        -------
        :obj:`ndarray`
            A ndarray of the data point.

        """
        if type(index) is int:
            return self.D.iloc[index].as_matrix()
        else:
            return self.D.loc[index].as_matrix()

    def getColumn(self, index):
        """Get a column of the dataframe.
 
        Parameters
        ----------
        index : int or string
            The index of the column in `D`, either positional or a string.

        Returns
        -------
        :obj:`ndarray`
            The values in the column.
        """
        if type(index) is int:
            return self.D.iloc[:, index].as_matrix()
        else:
            return self.D[index].as_matrix()

    def getColumnValues(self, index):
        """Get the unique values of a column.

        Parameters
        ----------
        index : int or string
            The index of the column in `D`, either positional or a string.

        Returns
        -------
        :obj:`ndarray`
            A ndarray of the unique values.

        """
        column = self.getColumn(index)
        if column.dtype == "float64":
            column = column[~np.isnan(column)]
        column = column[np.array([x != "NA" for x in column])]
        return np.unique(column)


    def getColumnDistribution(self, index):
        """Get the distribution of values in a column.

        Parameters
        ----------
        index : int or string
            The index of the column in `D`, either positional or a string.

        Returns
        -------
        :obj:`ndarray`, :obj:`ndarray`
            An array x of the unique labels, and an array y of the count of that label

        """
        x = self.getColumnValues(index)
        y = []
        



class DFDataSet:
    """A dataset living locally in a Pandas data frame.

    Columns of the Pandas data frame hold vectors of the same variable for all subjets, while
    rows of the Pandas data frame hold vectors of the same subject for all variables.

    The index of the dataframe should be whatever label you would like to appear on plots.

    Parameters
    ----------
    df_path : str
	Path to the .csv file describing the DiskDataSet.

    Attributes
    ----------
    dataframe : pandas DataFrame
        A DataFrame object describing the dataset.
    N : int
        The number of observations in the dataset.
    name : string
        A descriptive name for the dataset.

    """
    def __init__(self, dataframe, name = "mydataset"):
        self.D = dataframe
        self.N = dataframe.shape[0]
        self.name = name

    def getResource(self, index):
        """Get a specific data point from the data set.

        Parameters
        ----------
        index : int
            The index of the data point in `D`.

        Returns
        -------
        :obj:`ndarray`
            A ndarray of the data point.

        """
        return self.D.iloc[index].as_matrix().astype(float)


class DistanceMatrix:
    """A distance matrix computed from a DataSet object.

    Parameters
    ----------
    dataset : :obj:`DiskDataSet`
        A dataset on which to compute the distance matrix
    metric : function
        A distance used to compute the distance matrix.

    Attributes
    ----------
    dataset : :obj:`DiskDataSet`
        A dataset on which to compute the distance matrix
    metric : function
        A distance used to compute the distance matrix.
    N : int
        Number of data points in the dataset.
    matrix : :obj:`ndarray`
        The distance matrix.

    """

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
        """Get the distance matrix.

        Returns
        -------
        :obj:`ndarray`
            The distance matrix.

        """
        return self.matrix
