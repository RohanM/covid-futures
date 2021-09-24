import pytest

from app.lib.ml_model_data import MLModelData

def test_ml_model_data_mean(app, db_seeds):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.mean() == 110

def test_ml_model_data_std(app, db_seeds):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.std() == pytest.approx(107, 0.1)
