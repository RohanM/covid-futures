from torch import tensor

class Normalise:
    def perform(self, data):
        mean = self.__mean(data)
        std = self.__std(data)
        return { k:self.__normalise(v, mean, std) for k,v in data.items() }

    def __mean(self, data):
        return tensor(self.__flatten(data)).float().mean().item()

    def __std(self, data):
        return tensor(self.__flatten(data)).float().std(unbiased=False).item()

    def __flatten(self, data):
        return sum(data.values(), [])

    def __normalise(self, values, mean, std):
        return [(v - mean) / std for v in values]
