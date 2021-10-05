class Window:
    """
    Run a window of size (input_window+output_window) over the data, state by state,
    and build training data of the form: history => prediction.
    """
    def __init__(self, input_window=30, output_window=30):
        self.input_window = input_window
        self.output_window = output_window

    def perform(self, data):
        return { state:self.__window_state(data[state]) for state in self.__states(data) }

    def __window_state(self, data):
        window = self.input_window + self.output_window
        result = {'x': [], 'y': []}

        for i in range(len(data) - window + 1):
            result['x'].append(data[i:i+self.input_window])
            result['y'].append(data[i+self.input_window:i+window])
        return result

    def __states(self, data): return data.keys()
