import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pickle
import argparse
import multiprocessing

# Single Core

def orig_coherence(D, F_s=500):
    coherence = np.zeros((D.shape[0], D.shape[0]))
    for i in range(D.shape[0]):
        for j in range(i, D.shape[0]):
            coherence[i, j] = np.mean(signal.coherence(D[i, :], D[j, :], fs=500)[1])
            coherence[j, i] = coherence[i, j]
    return np.nan_to_num(coherence)

# Multi Core

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

# Driver

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='the input file')
    parser.add_argument('output_path', help='where to output image')
    parser.add_argument('cores', help='num cores to use')
    args = parser.parse_args()
    if args.cores == 'single':
        plt.imsave(args.output_path + '/coherence_single.png', orig_coherence(pickle.load(open(args.data, "rb"))))
    elif args.cores == 'multi':
        plt.imsave(args.output_path + '/coherence_multi.png', par_coherence(pickle.load(open(args.data, "rb"))))
    else:
        print 'BAD ARGUMENT FOR CORES: Use single or multi'

if __name__ == "__main__":
    main()
