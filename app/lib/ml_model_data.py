import numpy as np
from torch.utils.data import DataLoader
from functools import cached_property
from app import db
from app.lib.dataset import Dataset
from app.lib.models import Case

class MLModelData:
    def __init__(self, input_window=30, output_window=30, train_valid_split=0.8, batch_size=64):
        """
        input_window: Number of days of data used as input to the prediction
        output_window: Length of the prediction in days
        train_valid_split: What portion of data to use for training (the remainder is held back for validation)
        """
        self.input_window = input_window
        self.output_window = output_window
        self.train_valid_split = train_valid_split
        self.batch_size = batch_size

    def load(self):
        self.__load_cases()
        self.__calc_normalised_cases()
        self.__calc_windowed_cases()
        self.__split_train_valid()
        self.__combine_states()
        self.__init_dataloaders()

    @cached_property
    def mean(self):
        return np.mean(self.__all_cases())

    @cached_property
    def std(self):
        return np.std(self.__all_cases())

    def __all_cases(self):
        return sum(self.cases.values(), [])

    def __load_cases(self):
        self.cases = {}
        for state in Case.states():
            self.cases[state] = Case.confirmed_for_state(state)

    def __calc_normalised_cases(self):
        self.normalised_cases = { k:self.__normalise(v) for k,v in self.cases.items() }

    def __calc_windowed_cases(self):
        """Run a window of size (input_window+output_window) over the data, state by state,
        and build training data of the form: history => prediction
        """
        window = self.input_window + self.output_window
        self.x = {}
        self.y = {}
        for state in Case.states():
            self.x[state] = []
            self.y[state] = []
            state_data = self.normalised_cases[state]

            for i in range(len(state_data) - window + 1):
                self.x[state].append(state_data[i:i+self.input_window])
                self.y[state].append(state_data[i+self.input_window:i+window])

    def __split_train_valid(self):
        """Split data into training and validation sets"""
        self.train_x = { k:self.__split_one_train_valid(v, True) for k,v in self.x.items() }
        self.train_y = { k:self.__split_one_train_valid(v, True) for k,v in self.y.items() }
        self.valid_x = { k:self.__split_one_train_valid(v, False) for k,v in self.x.items() }
        self.valid_y = { k:self.__split_one_train_valid(v, False) for k,v in self.y.items() }

    def __combine_states(self):
        """Combine data from states and present in a Dataset"""
        self.all_train = Dataset(
            sum(self.train_x.values(), []),
            sum(self.train_y.values(), [])
        )
        self.all_valid = Dataset(
            sum(self.valid_x.values(), []),
            sum(self.valid_y.values(), [])
        )

    def __init_dataloaders(self):
        if len(self.all_train) > 0:
            self.dataloader_train = DataLoader(self.all_train, self.batch_size, shuffle=True)
        if len(self.all_valid) > 0:
            self.dataloader_valid = DataLoader(self.all_valid, self.batch_size, shuffle=False)

    def __normalise(self, values):
        return [(v - self.mean) / self.std for v in values]

    def __split_one_train_valid(self, values, is_training):
        train_len = int(len(values) * self.train_valid_split)
        return values[:train_len] if is_training else values[train_len:]
