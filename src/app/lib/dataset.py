import torch
from torch import tensor
from app.lib import get_device

class Dataset():
    def __init__(self, x, y):
        self.x = tensor(x).float().to(get_device())
        self.y = tensor(y).float().to(get_device())
    def __len__(self): return len(self.x)
    def __getitem__(self, i): return self.x[i], self.y[i]
    def __eq__(self, other):
        return isinstance(other, Dataset) and torch.all(self.x == other.x) and torch.all(self.y == other.y)
