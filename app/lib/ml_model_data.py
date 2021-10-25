from torch import tensor
from torch.utils.data import DataLoader
from functools import cached_property
from app import db
from app.lib import running_mean
from app.lib.dataset import Dataset
from app.lib.models import Case
from app.lib.data_pipeline import LoadCases, RunningMean, Normalise, Window, SplitTrainValid, FlattenStates, BuildDatasets, BuildDataloaders, Stats


class MLModelData:
    def __init__(self, running_mean_window=7, input_window=30, output_window=30, train_valid_split=0.8, batch_size=64):
        """
        Parameters:
        running_mean_window: Size of the window to generate the running mean
        input_window: Number of days of data used as input to the prediction
        output_window: Length of the prediction in days
        train_valid_split: What portion of data to use for training (the remainder is held back for validation)
        batch_size: Size of batch for the DataLoader to provide
        """
        self.data_pipeline = [
            LoadCases(),
            RunningMean(window=running_mean_window),
        ]
        self.stats_pipeline = self.data_pipeline + [
            Stats(),
        ]
        self.training_pipeline = self.data_pipeline + [
            Normalise(),
            Window(input_window=input_window, output_window=output_window),
            SplitTrainValid(split=train_valid_split),
            FlattenStates(),
            BuildDatasets({
                'train': ('train_x', 'train_y'),
                'valid': ('valid_x', 'valid_y'),
            }),
            BuildDataloaders({
                'train': { 'batch_size': batch_size, 'shuffle': True },
                'valid': { 'batch_size': batch_size, 'shuffle': False },
            }),
        ]

    def load(self):
        """
        Load training data and provide torch DataLoaders for training and validation.

        Main outputs:
        - self.dataloader_train
        - self.dataloader_valid
        """
        self.data = []
        for step in self.data_pipeline:
            self.data = step.perform(self.data)

        training_data = []
        for step in self.training_pipeline:
            training_data = step.perform(training_data)
        self.dataloader_train, self.dataloader_valid = training_data['train'], training_data['valid']

        stats = {}
        for step in self.stats_pipeline:
            stats = step.perform(stats)
        self.mean, self.std = stats['mean'], stats['std']
