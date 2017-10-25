import numpy as np

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools
import plotly.graph_objs as go

##################
# Main Driver Functions


# D: Dictionary of data for a given patient ['paradigm_name'] = [channels, values]
# p_global: Dictionary of global parameters
#     Sampling Frequency ['sample_freq'] X
#     Patient ID ['patient_id'] X
#     Paradigm Title Dictionary* ['title'] => get_title() ?
# p_local: Dictionary of local parameters
#     Downsample rate
#     Custom x, y bounds ['x_bounds'] => (min, max), ['y_bounds'] => (min, max) X
#         Have a set default
#     Range of channels to present ['disp_chans'] X
#     Slider or subplots ['is_slider'] X
#         If subplot, each subplot gets a row to itself

def sparklines(D, p_global, p_local):
    #############
    # Set params
    
    to_plot, params = \
        _get_params(D, p_global, p_local, 'Raw Sparklines')
    
    #############
    # Set layout
    
    # Setup titles
    xaxis = dict(
        title = 'Time (' + str(1. / p_global['sample_freq'] * params['downsample']) + ' seconds timestamps)',
        range = params['x_bounds']
    )
    yaxis = dict(
        title = 'Intensity (microVolts)',
        range = ['y_bounds']
    )
    
    layout = dict(title=params['title'], xaxis=xaxis, yaxis=yaxis)
    
    if params['is_slider']:
        layout['sliders'] = _make_slider(params['disp_chans'], 0)
    
    #############
    # Add data
    data = [dict(visible = False, mode = 'lines',
        x = np.arange(to_plot.shape[1] // params['downsample']),
        y = to_plot[i, ::params['downsample']]) for i in params['disp_chans']]
    data[0]['visible'] = True
    
    fig = dict(data=data, layout=layout)
    iplot(fig)

def spectrogram(D, p_global, p_local):
    #############
    # Set params
    
    to_plot, params = \
        _get_params(D, p_global, p_local, 'Raw Spectrograms')
    
    F_s = p_global['sample_freq']
    dt = 1./F_s
    
    #############
    # Set layout
    
    # Setup titles
    xaxis = dict(
        title = 'Frequency (Hz)',
        range = params['x_bounds']
    )
    yaxis = dict(
        title = 'Magnitude',
        range = params['y_bounds']
    )
    
    layout = dict(title=params['title'], xaxis=xaxis, yaxis=yaxis)
    
    if params['is_slider']:
        layout['sliders'] = _make_slider(params['disp_chans'], 0)
    
    #############
    # Add data
    data = []
    
    for i in params['disp_chans']:
        data.append(_make_spectrogram(to_plot, i, dt, params['downsample']))
    data[0]['visible'] = True
    
    fig = dict(data=data, layout=layout)
    iplot(fig)

def signal_heatmap(D, p_global, p_local):
    #############
    # Set params
    
    to_plot, params = \
        _get_params(D, p_global, p_local, 'Heatmap')
     
    if params['pc_proj'] is not None:
        params['title'] += " PC-PROJ = " + str(params['pc_proj'])
        U, _, _ = np.linalg.svd(to_plot, full_matrices=False)
        U = U[:, params['pc_proj'][0]:params['pc_proj'][1]]
        if not params['pc_collapse']:
            P = U.dot(U.T)
        else:
            P = U
            params['title'] += " COLLAPSED"
        to_plot = P.T.dot(to_plot)
    
    #############
    # Set layout
    
    # Setup titles
    xaxis = dict(
        title = 'Time (seconds)'
    )
    yaxis = dict(
        title = 'Channel'
    )
    
    layout = dict(title=params['title'], xaxis=xaxis, yaxis=yaxis)
     
    #############
    # Add data
    trace = go.Heatmap(z = to_plot[:, ::params['downsample']])
    data = [trace]
    
    fig = dict(data=data, layout=layout)
    iplot(fig)

def distance_matrix_heatmap(D, p_global, p_local):
    to_plot, params = \
        _get_params(D, p_global, p_local, '')
    params['title'] += params['metric'].__name__
    labels = [x for x in D.keys()]
    dataset = [x.T for x in D.values()]
    metric = params['metric'](dataset)
    dist_mat = getDistMat(metric)
    _square_heatmap(dist_mat, "paradigms", params['title']) 
    for i in range(len(labels)):
        print(i, labels[i])

def getDistMat(Metric):
    N = Metric.N
    dist_mat = np.zeros([N, N])
    for i in range(N):
        for j in range(N):
            dist_mat[i, j] = Metric.distance(i, j)
            dist_mat[j, i] = dist_mat[i, j] 
    return dist_mat

def correlation_heatmap(D, p_global, p_local):
    p_local['squarevar'] = "Channels" 
    to_plot, params = \
        _get_params(D, p_global, p_local, 'Correlation Matrix')
    with np.errstate(divide = 'ignore', invalid = 'ignore'):
        corr = np.nan_to_num(np.corrcoef(to_plot))
    _square_heatmap(corr, params["squarevar"], params["title"])

def covariance_heatmap(D, p_global, p_local):
    p_local['squarevar'] = "Channels"
    to_plot, params = \
        _get_params(D, p_global, p_local, 'Covariance Matrix')
    with np.errstate(divide = 'ignore', invalid = 'ignore'):
        corr = to_plot.dot(to_plot.T)
    _square_heatmap(corr, params["squarevar"], params["title"])

def scree_plot(D, p_global, p_local):
    to_plot, params = \
        _get_params(D, p_global, p_local, 'Scree Plot')
    _, spectrum, _ = np.linalg.svd(to_plot, full_matrices=False)
    scree = np.cumsum(spectrum) / np.sum(spectrum)
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
    layout = dict(title=params['title'], xaxis=xaxis, yaxis=yaxis)

    fig = dict(data=data, layout=layout)
    iplot(fig)



def _square_heatmap(D, squarevar, title):
    
    # Setup titles
    xaxis = dict(title = squarevar)
    yaxis = dict(title = squarevar)
    
    layout = dict(title=title, xaxis=xaxis, yaxis=yaxis, width=500, height=500)
     
    #############
    # Add data
    trace = go.Heatmap(z = D)
    data = [trace]
    
    fig = dict(data=data, layout=layout)
    iplot(fig)

def _make_slider(disp_chans, active):
    # Set different elecs as different ticks in slider
    steps = []
    for i in range(len(disp_chans)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(disp_chans)],
            label = disp_chans[i]
        )
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    # Setup slider with elecs
    sliders = [dict(
        active = active,
        currentvalue = {
            "prefix": "Electrode: "
        },
        pad = {"t": 50},
        steps = steps
    )]

    return sliders

# return to_plot, downsample, disp_chans, patient_id, title, is_slider, x_bounds, y_bounds
def _get_params(D, p_global, p_local, graph_title):
    
    # get data of specific paradigm to plot
    to_plot = D[p_local['paradigm']]
    
    params = dict()
    
    # downsample rate for PLOTTING
    params['downsample'] = int(p_local.get('downsample', 1))
    
    # set range of chans to visualize
    params['disp_chans'] = p_local.get('disp_chans', range(to_plot.shape[0]))
        
    # make title
    params['title'] = p_global['patient_id'] + ' ' + p_local['paradigm'] + ' ' +  graph_title

    # is slider
    params['is_slider'] = p_local.get('is_slider', True)
    
    # custom bounds
    params['x_bounds'] = list(p_local.get('x_bounds', []))
    params['y_bounds'] = list(p_local.get('y_bounds', []))

    params['pc_proj'] = p_local.get('pc_proj', None)
    params['pc_collapse'] = p_local.get('pc_collapse', False)

    params['squarevar'] = p_local.get('squarevar', "Variable")
    params['metric'] = p_local.get('metric', None)
    
    return to_plot, params 

def _make_spectrogram(data, chan, dt, downsample):
    sample_points = np.arange(data.shape[1]) * dt
    signal = data[chan, :]
    ft = np.fft.fft(signal) * dt
    ft = ft[: len(sample_points)/2]
    freq = np.fft.fftfreq(len(sample_points), dt)
    freq = freq[:len(sample_points)/2]

    return dict(
        visible = False,
        mode = 'markers',
        x = freq[:2000:downsample],
        y = np.abs(ft)[:2000:downsample]
    )
