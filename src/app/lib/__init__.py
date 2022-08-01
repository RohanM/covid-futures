import torch
import numpy as np

def running_mean(x, window=7):
    return np.convolve(x, np.ones(window) / window, mode='valid')

def get_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
