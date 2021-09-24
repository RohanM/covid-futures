import numpy as np
from functools import cached_property
from app import db
from app.lib.models import Case

class MLModelData:
    def load(self):
        self.__load_cases()
        self.__calc_normalised_cases()

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

    def __normalise(self, values):
        return [(v - self.mean) / self.std for v in values]
