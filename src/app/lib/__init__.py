import numpy as np

def running_mean(x, window=7):
    return np.convolve(x, np.ones(window) / window, mode='valid')
