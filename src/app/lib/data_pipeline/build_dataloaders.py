from torch.utils.data import DataLoader

class BuildDataloaders:
    """Put data into a PyTorch DataLoader"""
    def __init__(self, schema):
        """
        Parameters:
        schema: dict of { data_key: { dataloader_params } }
                eg. { 'all_train': { 'batch_size': 64, 'shuffle': False } }
        """
        self.schema = schema

    def perform(self, data):
        return { k:self.__build_dataloader(data[k], v) for k,v in self.schema.items() }

    def __build_dataloader(self, data, params):
        if len(data) < 1: return None
        return DataLoader(
            data,
            batch_size=params.get('batch_size', 1),
            shuffle=params.get('shuffle', False)
        )
