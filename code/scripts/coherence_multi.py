import numpy as np
import scipy.signal as signal
import time
import multiprocessing
import matplotlib.pyplot as plt
import pickle

NDARAA075AMK = {}
NDARAA075AMK['video1'] = pickle.load( open( "../../data/NDARAA075AMK/EEG/raw/PANDA/NDARAA075AMK_Video1_data.pkl", "rb" ) )

def par_coherence(D, F_s=500):
    NUM_WORKERS = multiprocessing.cpu_count() - 1
    
    coherence = np.zeros((D.shape[0], D.shape[0]))
    coherence_pars = [(i, j, D) for i in range(D.shape[0]) for j in range(i, D.shape[0])]
    
    pool = multiprocessing.Pool(processes=NUM_WORKERS)
    results = pool.map_async(get_coh, coherence_pars)
    coherence_vals = results.get()
    
    for ((i, j, D), val) in zip(coherence_pars, coherence_vals):
        coherence[i, j] = val
        coherence[j, i] = val
    
    return coherence

def get_coh(tup):
    i, j, D = tup[0], tup[1], tup[2]
    return np.mean(signal.coherence(D[i, :], D[j, :], fs=500)[1])

plt.imsave( './coherence_multi_core.png', par_coherence(NDARAA075AMK['video1'])[0])
