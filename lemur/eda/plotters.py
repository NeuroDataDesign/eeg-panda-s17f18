from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools
import plotly.graph_objs as go
import numpy as np

import lemur.utils.io as lio

BASETITLE = '''
<b>%s - %s - %s - %s</b>
'''

class BasePlotter(lio.BIDSDataset):
    def getTitle(self, sub, task):
        title = BASETITLE % (self.Meta["dataset_name"],
                             self.subjects[sub],
                             self.tasks[task],
                             self.plotname)
        return title


class ScreePlotter(BasePlotter):
    plotname = "Scree Plot"

    def plot(self, sub, task):
        title = self.getTitle(sub, task)
        D = self.getData(sub, task)
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
    def plot(self, sub, task):
        title = self.getTitle(sub, task)
        D = self.getData(sub, task)
        D_square = self.squareComputation(D)
        xaxis = dict(title = self.Meta['row_variable'])
        yaxis = dict(title = self.Meta['row_variable'])
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
