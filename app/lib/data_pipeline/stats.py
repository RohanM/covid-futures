from torch import tensor

class Stats:
    def perform(self, data):
        return {
            'mean': self.__mean(data),
            'std': self.__std(data),
        }

    def __mean(self, data):
        return tensor(self.__flatten(data)).float().mean().item()

    def __std(self, data):
        return tensor(self.__flatten(data)).float().std(unbiased=False).item()

    def __flatten(self, data):
        return sum(data.values(), [])
