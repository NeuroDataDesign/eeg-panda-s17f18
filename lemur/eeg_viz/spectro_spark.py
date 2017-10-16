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
        title = 'Time (' + str(1. / p_global['sample_freq'] * downsample) + ' seconds timestamps)',
        range = x_bounds
    )
    yaxis = dict(
        title = 'Intensity (microVolts)',
        range = y_bounds
    )
    
    layout = dict(title=title, xaxis=xaxis, yaxis=yaxis)
    
    if params['is_slider']:
        layout['sliders'] = _make_slider(params['disp_chans'], 0)
    
    #############
    # Add data
    data = [dict(
        visible = False,
        mode = 'markers',
        x = range(to_plot.shape[1] / downsample),
        y = to_plot[i, ::downsample]) for i in params['disp_chans']
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
        range = x_bounds
    )
    yaxis = dict(
        title = 'Magnitude',
        range = y_bounds
    )
    
    layout = dict(title=title, xaxis=xaxis, yaxis=yaxis)
    
    if params['is_slider']:
        layout['sliders'] = _make_slider(params['disp_chans'], 0)
    
    #############
    # Add data
    data = []
    
    for i in params['disp_chans']:
        data.append(_make_spectrogram(to_plot, i, dt, downsample))
    data[0]['visible'] = True
    
    fig = dict(data=data, layout=layout)
    iplot(fig)

####################################
# Helper functions

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
    params['downsample'] = p_local.get('downsample', 1)
    
    # set range of chans to visualize
    params['disp_chans'] = p_local.get('disp_chans', range(to_plot.shape[0]))
        
    # make title
    params['title'] = 'Patient ' + p_global['patient_id'] + ' ' +    \
        p_global['title'].get(p_local['paradigm'], p_local['paradigm']) + ' ' + graph_title

    # is slider
    params['is_slider'] = p_local.get('is_slider', True)
    
    # custom bounds
    params['x_bounds'] = list(p_local.get('x_bounds', []))
    params['y_bounds'] = list(p_local.get('y_bounds', []))
    
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
