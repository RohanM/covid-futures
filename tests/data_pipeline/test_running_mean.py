import pytest
from app.lib.data_pipeline import RunningMean

def test_running_mean():
    data = {
        'NSW': [100, 200, 300, 400, 500],
        'VIC': [10, 20, 30, 40, 50],
    }
    assert RunningMean(window=2).perform(data) == {
        'NSW': [150, 250, 350, 450],
        'VIC': [15, 25, 35, 45],
    }
