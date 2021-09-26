import pytest
from torch.utils.data import DataLoader

from app.lib.ml_model_data import MLModelData

@pytest.fixture
def normalised_extended_cases():
    """Map values in db_extended_cases to normalised values"""
    return {
        10: pytest.approx(-0.92, abs=0.01),
        20: pytest.approx(-0.86, abs=0.01),
        30: pytest.approx(-0.80, abs=0.01),
        40: pytest.approx(-0.74, abs=0.01),
        50: pytest.approx(-0.68, abs=0.01),
        100: pytest.approx(-0.39, abs=0.01),
        200: pytest.approx(0.21, abs=0.01),
        300: pytest.approx(0.80, abs=0.01),
        400: pytest.approx(1.40, abs=0.01),
        500: pytest.approx(1.99, abs=0.01),
    }


def test_data_mean(app, db_simple_cases):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.mean == 110

def test_data_std(app, db_simple_cases):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.std == pytest.approx(107, 0.1)

def test_normalised_cases(app, db_extended_cases, normalised_extended_cases):
    with app.app_context():
        data = MLModelData()
        data.load()
        assert data.normalised_cases == {
            'NSW': [
                normalised_extended_cases[100],
                normalised_extended_cases[200],
                normalised_extended_cases[300],
                normalised_extended_cases[400],
                normalised_extended_cases[500],
            ],
            'VIC': [
                normalised_extended_cases[10],
                normalised_extended_cases[20],
                normalised_extended_cases[30],
                normalised_extended_cases[40],
                normalised_extended_cases[50],
            ],
        }

def test_windowed_cases(app, db_extended_cases, normalised_extended_cases):
    with app.app_context():
        data = MLModelData(input_window=2, output_window=2)
        data.load()
        assert data.x == {
            'NSW': [
                [normalised_extended_cases[100], normalised_extended_cases[200]],
                [normalised_extended_cases[200], normalised_extended_cases[300]],
            ],
            'VIC': [
                [normalised_extended_cases[10], normalised_extended_cases[20]],
                [normalised_extended_cases[20], normalised_extended_cases[30]],
            ],
        }
        assert data.y == {
            'NSW': [
                [normalised_extended_cases[300], normalised_extended_cases[400]],
                [normalised_extended_cases[400], normalised_extended_cases[500]],
            ],
            'VIC': [
                [normalised_extended_cases[30], normalised_extended_cases[40]],
                [normalised_extended_cases[40], normalised_extended_cases[50]],
            ]
        }

def test_split_train_validation(app, db_extended_cases):
    with app.app_context():
        data = MLModelData(input_window=1, output_window=1, train_valid_split=0.75)
        data.load()
        assert len(data.train_x['NSW']) == 3
        assert len(data.train_x['VIC']) == 3
        assert len(data.train_y['NSW']) == 3
        assert len(data.train_y['VIC']) == 3
        assert len(data.valid_x['NSW']) == 1
        assert len(data.valid_x['VIC']) == 1
        assert len(data.valid_y['NSW']) == 1
        assert len(data.valid_y['VIC']) == 1

def test_combine_data(app, db_extended_cases):
    with app.app_context():
        data = MLModelData(input_window=1, output_window=1, train_valid_split=0.75)
        data.load()
        assert len(data.all_train.x) == 6
        assert len(data.all_train.y) == 6
        assert len(data.all_valid.x) == 2
        assert len(data.all_valid.y) == 2

def test_dataloader(app, db_extended_cases):
    with app.app_context():
        data = MLModelData(input_window=1, output_window=1, train_valid_split=0.75)
        data.load()
        assert type(data.dataloader_train) == DataLoader
        assert type(data.dataloader_valid) == DataLoader
