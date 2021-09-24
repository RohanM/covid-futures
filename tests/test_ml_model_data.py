import pytest

from app.lib.ml_model_data import MLModelData

def test_ml_model_data_mean(app, db_seeds):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.mean == 110

def test_ml_model_data_std(app, db_seeds):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.std == pytest.approx(107, 0.1)

def test_ml_model_normalised_cases(app, db_seeds):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.normalised_cases == {
            'NSW': [pytest.approx(-0.09, abs=0.01), pytest.approx(0.84, abs=0.01), pytest.approx(1.77, abs=0.01)],
            'VIC': [pytest.approx(-0.93, abs=0.01), pytest.approx(-0.84, abs=0.01), pytest.approx(-0.75, abs=0.01)],
        }
