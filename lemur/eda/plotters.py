from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools
import plotly.graph_objs as go
import numpy as np


class BasePlotter:
    def __init__(self, data):
        self.data = data

    def getInfo(self, *args, **kwargs):
        D = self.data.getData(*args, **kwargs)
        titleheader = self.data.getTitleHeader(*args, **kwargs)
        return D, titleheader

class ScreePlotter(BasePlotter):
    plotname = "Scree Plot"

    def plot(self, *args, **kwargs):
        D, titleheader = self.getInfo(*args, **kwargs)
        title = titleheader + self.plotname 
        _, S, _ = np.linalg.svd(D, full_matrices=False)
        scree = np.cumsum(S) / np.sum(S)
        scree = scree[scree < .999]
        xaxis = dict(
            title = 'PC number'
        )
        yaxis = dict(
            title = 'Cum. variance explained'
        )
        data = [dict(mode = 'line',
                 x = np.arange(len(scree)),
                 y = scree)] 
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis)
        fig = dict(data=data, layout=layout)
        iplot(fig)

class SquareMatrixPlotter(BasePlotter):
    def plot(self, *args, **kwargs):
        D, titleheader = self.getInfo(*args, **kwargs)
        title = titleheader + self.plotname 
        D_square = self.squareComputation(D)
        xaxis = dict(title = self.data.Meta['row_variable'])
        yaxis = dict(title = self.data.Meta['row_variable'])
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis, width=600, height=600)
     
        trace = go.Heatmap(z = D_square)
        data = [trace]
    
        fig = dict(data=data, layout=layout)
        iplot(fig)

class CorrelationMatrixPlotter(SquareMatrixPlotter):
    plotname = "Correlation Matrix"

    def squareComputation(self, D):
        with np.errstate(divide = 'ignore', invalid = 'ignore'):
            corr = np.nan_to_num(np.corrcoef(D))
        return corr

class CovarianceMatrixPlotter(SquareMatrixPlotter):
    plotname = "Covariance Matrix"

    def squareComputation(self, D):
        with np.errstate(divide = 'ignore', invalid = 'ignore'):
            cov = D.dot(D.T)
        return cov
