from app.lib import running_mean

class RunningMean:
    def __init__(self, window):
        self.window = window

    def perform(self, data):
        return { k:list(running_mean(v, window=self.window)) for k,v in data.items() }
