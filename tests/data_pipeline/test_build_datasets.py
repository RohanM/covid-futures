import pytest
from app.lib.dataset import Dataset
from app.lib.data_pipeline import BuildDatasets

def test_build_datasets():
    data = {
        'train_x': [100, 200, 300, 10, 20, 30],
        'train_y': [200, 300, 400, 20, 30, 40],
        'valid_x': [400, 40],
        'valid_y': [500, 50],
    }
    assert BuildDatasets({
        'all_train': ('train_x', 'train_y'),
        'all_valid': ('valid_x', 'valid_y'),
    }).perform(data) == {
        'all_train': Dataset(
            [100, 200, 300, 10, 20, 30],
            [200, 300, 400, 20, 30, 40],
        ),
        'all_valid': Dataset(
            [400, 40],
            [500, 50],
        ),
    }
