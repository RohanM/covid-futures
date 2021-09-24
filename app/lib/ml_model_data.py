import numpy as np
from app import db
from app.lib.models import Case

class MLModelData:
    def load(self):
        self.__load_cases()

    def mean(self):
        return np.mean(
            [np.mean(state_cases) for _,state_cases in self.cases.items()]
        )

    def __load_cases(self):
        self.cases = {}
        for state in Case.states():
            self.cases[state] = Case.confirmed_for_state(state)
