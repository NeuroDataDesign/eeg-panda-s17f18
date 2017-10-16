import numpy as np

def divideMatrixIntoChunks(mat, n_chunks):
    L = mat.shape[0] - (mat.shape[0] % n_chunks)
    sublen = L // n_chunks
    chunks = []
    for i in range(0, L, sublen):
        chunks.append(mat[i:i+sublen, :])
    return chunks

def generateRandomTimeSeries(d, T, strength = 5):
    preference = np.exp(np.abs(np.random.normal(0, strength, d)))
    preference = preference / np.linalg.norm(preference)
    start = np.random.normal(0, preference, d) * np.sqrt(T)
    curr = start
    states = []
    for i in range(T):
        curr = curr + np.random.normal(0, preference, d)
        states.append(curr)
    return np.column_stack(states).T

