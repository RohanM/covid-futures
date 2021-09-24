import numpy as np
from app import db
from app.lib.models import Case

class MLModelData:
    def load(self):
        self.__load_cases()

    def mean(self):
        return np.mean(self.__all_cases())

    def std(self):
        return np.std(self.__all_cases())

    def __all_cases(self):
        return sum(self.cases.values(), [])

    def __load_cases(self):
        self.cases = {}
        for state in Case.states():
            self.cases[state] = Case.confirmed_for_state(state)
