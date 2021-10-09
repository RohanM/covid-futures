import pytest
from app.lib.data_pipeline import SplitTrainValid

def test_split_train_valid():
    data = {
        'NSW': {
            'x': [100, 200, 300, 400],
            'y': [200, 300, 400, 500],
        },
        'VIC': {
            'x': [10, 20, 30, 40],
            'y': [20, 30, 40, 50],
        },
    }
    assert SplitTrainValid(split=0.75).perform(data) == {
        'NSW': {
            'train_x': [100, 200, 300],
            'train_y': [200, 300, 400],
            'valid_x': [400],
            'valid_y': [500],
        },
        'VIC': {
            'train_x': [10, 20, 30],
            'train_y': [20, 30, 40],
            'valid_x': [40],
            'valid_y': [50],
        },
    }
