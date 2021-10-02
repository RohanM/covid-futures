from torch import tensor
from torch.utils.data import DataLoader
from functools import cached_property
from app import db
from app.lib.dataset import Dataset
from app.lib.models import Case

class MLModelData:
    def __init__(self, input_window=30, output_window=30, train_valid_split=0.8, batch_size=64):
        """
        Parameters:
        input_window: Number of days of data used as input to the prediction
        output_window: Length of the prediction in days
        train_valid_split: What portion of data to use for training (the remainder is held back for validation)
        batch_size: Size of batch for the DataLoader to provide
        """
        self.input_window = input_window
        self.output_window = output_window
        self.train_valid_split = train_valid_split
        self.batch_size = batch_size

    def load(self):
        """
        Load training data and provide torch DataLoaders for training and validation.

        Main outputs:
        - self.dataloader_train
        - self.dataloader_valid
        """
        self.cases = self.__load_cases()
        self.normalised_cases = self.__calc_normalised_cases(self.cases)
        self.x, self.y = self.__calc_windowed_cases(self.normalised_cases)
        self.train_x, self.train_y, self.valid_x, self.valid_y = self.__split_train_valid(self.x, self.y)
        self.all_train, self.all_valid = self.__combine_states(self.train_x, self.train_y, self.valid_x, self.valid_y)
        self.dataloader_train, self.dataloader_valid = self.__init_dataloaders(self.all_train, self.all_valid)

    @cached_property
    def mean(self):
        return tensor(self.__all_cases()).float().mean().item()

    @cached_property
    def std(self):
        return tensor(self.__all_cases()).float().std(unbiased=False).item()

    def __all_cases(self):
        return sum(self.cases.values(), [])

    def __load_cases(self):
        cases = {}
        for state in Case.states():
            cases[state] = Case.confirmed_for_state(state)
        return cases

    def __calc_normalised_cases(self, cases):
        return { k:self.__normalise(v) for k,v in cases.items() }

    def __calc_windowed_cases(self, normalised_cases):
        """Run a window of size (input_window+output_window) over the data, state by state,
        and build training data of the form: history => prediction
        """
        window = self.input_window + self.output_window
        x = {}
        y = {}
        for state in Case.states():
            x[state] = []
            y[state] = []
            state_data = normalised_cases[state]

            for i in range(len(state_data) - window + 1):
                x[state].append(state_data[i:i+self.input_window])
                y[state].append(state_data[i+self.input_window:i+window])
        return x, y

    def __split_train_valid(self, x, y):
        """Split data into training and validation sets"""
        train_x = { k:self.__split_one_train_valid(v, True) for k,v in x.items() }
        train_y = { k:self.__split_one_train_valid(v, True) for k,v in y.items() }
        valid_x = { k:self.__split_one_train_valid(v, False) for k,v in x.items() }
        valid_y = { k:self.__split_one_train_valid(v, False) for k,v in y.items() }
        return train_x, train_y, valid_x, valid_y

    def __combine_states(self, train_x, train_y, valid_x, valid_y):
        """Combine data from states and present in a Dataset"""
        all_train = Dataset(
            tensor(sum(train_x.values(), [])).float(),
            tensor(sum(train_y.values(), [])).float(),
        )
        all_valid = Dataset(
            tensor(sum(valid_x.values(), [])).float(),
            tensor(sum(valid_y.values(), [])).float(),
        )
        return all_train, all_valid

    def __init_dataloaders(self, all_train, all_valid):
        dataloader_train, dataloader_valid = None, None
        if len(all_train) > 0:
            dataloader_train = DataLoader(all_train, self.batch_size, shuffle=True)
        if len(all_valid) > 0:
            dataloader_valid = DataLoader(all_valid, self.batch_size, shuffle=False)
        return dataloader_train, dataloader_valid

    def __normalise(self, values):
        return [(v - self.mean) / self.std for v in values]

    def __split_one_train_valid(self, values, is_training):
        train_len = int(len(values) * self.train_valid_split)
        return values[:train_len] if is_training else values[train_len:]
