import sys
import pandas as pd
import numpy as np
import pickle as pkl

def main(inpath, outpath):
    d = pd.read_csv(inpath, dtype=np.float32).as_matrix()
    with open(outpath, 'wb') as f:
        pkl.dump(d, f, protocol=pkl.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    _, inpath, outpath = sys.argv
    main(inpath, outpath)
