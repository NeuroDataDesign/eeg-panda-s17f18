from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lemur.distance.functions import energy_distance


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
        y = S
        x = np.arange(1, len(S) + 1)
        sy = np.sum(y)
        cy = np.cumsum(y)
        xaxis = dict(
            title = 'Factors'
        )
        yaxis = dict(
            title = 'Proportion of Total Variance'
        )
        var = go.Scatter(mode = 'lines+markers',
                         x = x,
                         y = y / sy,
                         name = "Variance")
        cumvar = go.Scatter(mode = 'lines+markers',
                            x = x,
                            y = cy / sy,
                            name = "Cumulative Variance")
        data = [var, cumvar]
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

class EnergyDistanceMatrixPlotter(SquareMatrixPlotter):
    plotname = "Energy Distance Matrix"

    def squareComputation(self, D):
        d, n = D.shape
        ed = np.empty([d, d])
        for i in range(d):
            for j in range(i + 1):
                if len(D[i, :]) > 1000:
                    x = np.random.choice(D[i, :], size = 1000)
                else:
                    x = D[i, :]
                if len(D[j, :]) > 1000:
                    y = np.random.choice(D[j, :], size = 1000)
                else:
                    x = D[j, :]
                ed[i, j] = energy_distance(x, y)
                ed[j, i] = ed[i, j]
        return ed

class EigenvectorPairsPlotter(BasePlotter):
    plotname = "Eigenvectors Pairs Plot"

    def plot(self, *args, **kwargs):
        D, titleheader = self.getInfo(*args, **kwargs)
        title = titleheader + self.plotname 
        U, _, _ = np.linalg.svd(D, full_matrices=False)
        U = U[:, :5]
        P = U.T.dot(D)
        Pdf = pd.DataFrame(P.T, columns = ["PC" + str(x) for x in range(1, 5 + 1)])
        sns.pairplot(data=Pdf, diag_kind="kde", markers="+",
                     diag_kws=dict(shade=True), kind='reg')
        plt.subplots_adjust(top=0.9)
        plt.suptitle(title)
        plt.show()
