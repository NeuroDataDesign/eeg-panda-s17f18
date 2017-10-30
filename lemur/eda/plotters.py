from plotly.offline import iplot
import plotly.figure_factory as ff
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.html.widgets import interact

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from lemur.distance.functions import energy_distance
from lemur.eda.reducers import PCA


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
        _, S, _, _ = PCA(D)
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
        U, _, _, mu = PCA(D)
        U = U[:, :3]
        P = U.T.dot(D - mu) + U.T.dot(mu)
        Pdf = pd.DataFrame(P.T, columns = ["PC" + str(x) for x in range(1, 3 + 1)])
        if Pdf.shape[0] > 500:
            g = sns.PairGrid(Pdf)
            g.map_diag(plt.hist)
            g.map_offdiag(plt.hexbin,
                          linewidths=0,
                          gridsize=20,
                          bins = 'log',
                          cmap=sns.light_palette("blue", as_cmap=True))
        else:
            sns.pairplot(data=Pdf, diag_kind="kde", markers="+",
                         diag_kws=dict(shade=True), kind='reg')
        plt.subplots_adjust(top=0.9)
        plt.suptitle(title)
        plt.show()

class HeatmapPlotter(BasePlotter):
    plotname = "Heatmap Plot"

    def plot(self, *args, **kwargs):
        D, titleheader = self.getInfo(*args, **kwargs)
        title = titleheader + self.plotname 
        U, s, _, mu = PCA(D)
        cv = np.cumsum(s)
        P = U[:, s < .9]
        D = P.T.dot(D - mu) + P.T.dot(mu)
        if D.shape[1] > 1000:
            kmeans = KMeans(n_clusters = 1000,
                            max_iter = 5,
                            n_init = 4,
                            n_jobs = 4,
                            algorithm = "elkan",
                            random_state = 123).fit(D.T)
            centers = kmeans.cluster_centers_
            samples = []
            for c in centers:
                s = np.argmin(np.linalg.norm(D.T - c, axis=1))
                samples.append(s) 
            D = D[:, samples]

        xaxis = dict(title = "Samples closest to 1000 k-means centers")
        yaxis = dict(title = "PCA Dims with <.9 cum. var. explained")
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis, width=600, height=600) 
        trace = go.Heatmap(z = D)
        data = [trace]
        fig = dict(data=data, layout=layout)
        iplot(fig)

class ParallelCoordinatePlotter(BasePlotter):
    plotname = "Parallel Coordinate Plot"

    def plot(self, *args, **kwargs):
        D, titleheader = self.getInfo(*args, **kwargs)
        title = titleheader + self.plotname 
        U, s, _, mu = PCA(D)
        P = U[:, :5]
        D = P.T.dot(D - mu)
        d, n = D.shape
        D = D - np.min(D, axis=1).reshape(d, 1)
        D = D / np.max(D, axis=1).reshape(d, 1)
        def view_plot(w1, w2):
            dims = [dict(label = "PC" + str(x),
                         values = D[x, :]) for x in range(5)]
            dims[0]["constraintrange"] = [w1, w2]
            trace = go.Parcoords(dimensions = list(dims))
            data = [trace]
            fig = dict(data = data)
            iplot(fig)
        return interact(view_plot, w1=(0, 1), w2=(0, 1))

class DendogramPlotter(BasePlotter):
    plotname = "Dendogram Plot"

    def plot(self, *args, **kwargs):
        D, titleheader = self.getInfo(*args, **kwargs)
        title = titleheader + self.plotname 
        dendro = ff.create_dendrogram(D)
        dendro['layout'].update({'width':800, 'height':500})
        iplot(dendro)
