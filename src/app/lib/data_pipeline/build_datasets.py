from app.lib.dataset import Dataset

class BuildDatasets:
    """Bundle (x, y) data into Dataset classes"""
    def __init__(self, schema):
        """
        Parameters:
        schema: dict of {key: (x_key, y_key), ...}
                eg. { 'all_train': ('train_x', 'train_y') }
        """
        self.schema = schema

    def perform(self, data):
        return { k:Dataset(data[v[0]], data[v[1]]) for k,v in self.schema.items() }
