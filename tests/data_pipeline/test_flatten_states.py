import pytest
from app.lib.data_pipeline import FlattenStates

def test_flatten_states():
    data = {
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
    assert FlattenStates().perform(data) == {
        'train_x': [100, 200, 300, 10, 20, 30],
        'train_y': [200, 300, 400, 20, 30, 40],
        'valid_x': [400, 40],
        'valid_y': [500, 50],
    }
