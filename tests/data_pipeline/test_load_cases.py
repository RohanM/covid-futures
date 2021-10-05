import pytest
from app.lib.data_pipeline import LoadCases

def test_load_cases(app, db_simple_cases):
    with app.app_context():
        assert LoadCases().perform() == {
            'NSW': [100, 200, 300],
            'VIC': [10, 20, 30]
        }

def test_ignores_data(app, db_simple_cases):
    with app.app_context():
        assert LoadCases().perform([]) == {
            'NSW': [100, 200, 300],
            'VIC': [10, 20, 30]
        }
