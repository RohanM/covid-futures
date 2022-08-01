import torch

class SaveToPT:
    def perform(self, data):
        torch.save(data, 'data.pt')
        return data

class LoadFromPT:
    def perform(self, data=None):
        return torch.load('data.pt')
