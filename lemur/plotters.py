from plotly.offline import iplot
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class DistanceMatrixPlotter:

    def __init__(self, dm, primary_label = "resource_path"):
        self.dataset_name = dm.dataset.name
        self.dm = dm.getMatrix()
        self.label_name = primary_label
        self.label = dm.dataset.D[primary_label]
        self.metric_name = dm.metric.__name__


class DistanceMatrixHeatmap(DistanceMatrixPlotter):
    titlestring = "%s Distance Matrix Heatmap under %s metric"

    def plot(self):
        title = self.titlestring % (self.dataset_name, self.metric_name)
        xaxis = go.XAxis(
                ticktext = self.label,
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        yaxis = go.YAxis(
                ticktext = self.label,
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis, width=600, height=600)
        trace = go.Heatmap(z = self.dm)
        data = [trace]
        fig = dict(data=data, layout=layout)
        iplot(fig)

class Embedding2DScatter(DistanceMatrixPlotter):
    titlestring = "%s embedding of %s distance matrix 2D scatter"

    def plot(self, embedder):
        title = self.titlestring % (embedder.embedding_name, self.metric_name)
        emb = embedder.embed(self.dm)
        d = {
            'factor 1': emb[:, 0],
            'factor 2': emb[:, 1],
            self.label_name: self.label
        }
        D = pd.DataFrame(d)
        sns.lmplot('factor 1',
                   'factor 2',
                    data = D,
                    fit_reg = False,
                    hue=self.label_name)
        plt.title(title)
        plt.show()

class EmbeddingPairsPlotter(DistanceMatrixPlotter):
    titlestring = "%s embedding of %s distance matrix Pairs Plot"

    def plot(self, embedder):
        title = self.titlestring % (embedder.embedding_name, self.metric_name)
        emb = embedder.embed(self.dm)
        Pdf = pd.DataFrame(emb, columns = ["factor %s"%x for x in range(1, emb.shape[1] + 1)])
        Pdf[self.label_name] = self.label
        sns.pairplot(data=Pdf, hue=self.label_name, diag_kind="hist")
        plt.subplots_adjust(top=0.9)
        plt.suptitle(title)
        plt.show()
