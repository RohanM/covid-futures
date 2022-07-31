from functools import reduce

class FlattenStates:
    """Combine data from states"""
    def perform(self, data):
        return reduce(self.__flatten, data.values())

    def __flatten(self, s1, s2):
        keys = set(list(s1.keys()) + list(s2.keys()))
        return { k:sum([s1.get(k, []), s2.get(k, [])], []) for k in keys }
