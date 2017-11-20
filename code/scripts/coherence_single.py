import numpy as np
import scipy.signal as signal
import time
import matplotlib.pyplot as plt
import pickle
import argparse

NDARAA075AMK = {}
NDARAA075AMK['video1'] = pickle.load( open( "../../data/NDARAA075AMK/EEG/raw/PANDA/NDARAA075AMK_Video1_data.pkl", "rb" ) )

def orig_coherence(D, F_s=500):
    times = []
    coherence = np.zeros((D.shape[0], D.shape[0]))
    for i in range(D.shape[0]):
        for j in range(i, D.shape[0]):
            start = time.time()
            coherence[i, j] = np.mean(signal.coherence(D[i, :], D[j, :], fs=500)[1])
            coherence[j, i] = coherence[i, j]
            end = time.time()
            times.append(end - start)
    return np.nan_to_num(coherence), times


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='the input file')
    parser.add_argument('output', help='the input file')
    args = parser.parse_args()
    plt.imsave(args.output, orig_coherence(pickle.load(open(args.data, "rb")))[0])

if __name__ == "__main__":
    main()
