import pytest
from app.lib.data_pipeline import Window

def test_windowed_cases():
    data = {
        'NSW': [100, 200, 300, 400, 500],
        'VIC': [10, 20, 30, 40, 50],
    }
    assert Window(input_window=2, output_window=2).perform(data) == {
        'NSW': {
            'x': [[100, 200], [200, 300]],
            'y': [[300, 400], [400, 500]],
        },
        'VIC': {
            'x': [[10, 20], [20, 30]],
            'y': [[30, 40], [40, 50]],
        },
    }
