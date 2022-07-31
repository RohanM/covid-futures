from app.lib.models import Case

class LoadCases:
    def perform(self, data=None):
        cases = {}
        for state in Case.states():
            cases[state] = Case.confirmed_for_state(state)
        return cases
