import pytest
from app.lib.data_pipeline import Normalise

@pytest.fixture
def normalised_cases():
    """Map case numbers to normalised values"""
    return {
        10: pytest.approx(-0.93, abs=0.01),
        20: pytest.approx(-0.84, abs=0.01),
        30: pytest.approx(-0.75, abs=0.01),
        100: pytest.approx(-0.09, abs=0.01),
        200: pytest.approx(0.84, abs=0.01),
        300: pytest.approx(1.77, abs=0.01),
    }

def test_normalise(normalised_cases):
    data = {
        'NSW': [100, 200, 300],
        'VIC': [10, 20, 30],
    }
    assert Normalise().perform(data) == {
        'NSW': [normalised_cases[100], normalised_cases[200], normalised_cases[300]],
        'VIC': [normalised_cases[10], normalised_cases[20], normalised_cases[30]],
    }
