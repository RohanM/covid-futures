class SplitTrainValid:
    """Split data into training and validation sets"""
    def __init__(self, split=0.8):
        self.split = split

    def perform(self, data):
        return { k:self.__split_state(v) for k,v in data.items() }

    def __split_state(self, data):
        return {
            'train_x': self.__split_data(data['x'], True),
            'train_y': self.__split_data(data['y'], True),
            'valid_x': self.__split_data(data['x'], False),
            'valid_y': self.__split_data(data['y'], False),
        }

    def __split_data(self, values, is_training):
        train_len = int(len(values) * self.split)
        return values[:train_len] if is_training else values[train_len:]
