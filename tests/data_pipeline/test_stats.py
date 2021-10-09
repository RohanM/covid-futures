import pytest
from app.lib.data_pipeline import Stats

def test_stats():
    data = {
        'NSW': [100, 200, 300],
        'VIC': [10, 20, 30],
    }
    assert Stats().perform(data) == {
        'mean': 110,
        'std': pytest.approx(107, abs=0.1),
    }
