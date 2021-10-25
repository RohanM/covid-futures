import pytest
from torch.utils.data import DataLoader
from app.lib.dataset import Dataset

from app.lib.ml_model_data import MLModelData

@pytest.fixture
def normalised_cases():
    """Map case numbers to normalised values"""
    return {
        10: pytest.approx(0.04, abs=0.01),

        15: pytest.approx(-0.94, abs=0.01),
        25: pytest.approx(-0.90, abs=0.01),
        35: pytest.approx(-0.85, abs=0.01),
        45: pytest.approx(-0.81, abs=0.01),
        55: pytest.approx(-0.76, abs=0.01),
        65: pytest.approx(-0.71, abs=0.01),

        100: pytest.approx(0.46, abs=0.01),

        150: pytest.approx(-0.32, abs=0.01),
        250: pytest.approx(0.14, abs=0.01),
        350: pytest.approx(0.60, abs=0.01),
        450: pytest.approx(1.06, abs=0.01),
        550: pytest.approx(1.52, abs=0.01),
        650: pytest.approx(1.98, abs=0.01),
    }


def test_data_mean(app, db_simple_cases):
    with app.app_context():
        data = MLModelData(running_mean_window=1)
        data.load()
        assert data.mean == 110

def test_data_std(app, db_simple_cases):
    with app.app_context():
        data = MLModelData(running_mean_window=1)
        data.load()
        assert data.std == pytest.approx(107, 0.1)

def test_data(app, db_simple_cases):
    with app.app_context():
        data = MLModelData(running_mean_window=1)
        data.load()
        assert data.data == {
            'NSW': [100.0, 200.0, 300.0],
            'VIC': [10.0, 20.0, 30.0],
        }

def test_dataloaders(app, db_extended_cases):
    with app.app_context():
        data = MLModelData(running_mean_window=2, input_window=1, output_window=1, train_valid_split=0.6)
        data.load()
        assert type(data.dataloader_train) == DataLoader
        assert type(data.dataloader_valid) == DataLoader

def test_dataloader_data(app, db_extended_cases, normalised_cases):
    with app.app_context():
        data = MLModelData(running_mean_window=2, input_window=1, output_window=1, train_valid_split=0.6)
        data.load()
        assert data.dataloader_train.dataset.x.tolist() == [
            [normalised_cases[150]],
            [normalised_cases[250]],
            [normalised_cases[350]],
            [normalised_cases[15]],
            [normalised_cases[25]],
            [normalised_cases[35]],
        ]
        assert data.dataloader_train.dataset.y.tolist() == [
            [normalised_cases[250 - 150]],
            [normalised_cases[350 - 250]],
            [normalised_cases[450 - 350]],
            [normalised_cases[25 - 15]],
            [normalised_cases[35 - 25]],
            [normalised_cases[45 - 35]],
        ]
        assert data.dataloader_valid.dataset.x.tolist() == [
            [normalised_cases[450]],
            [normalised_cases[550]],
            [normalised_cases[45]],
            [normalised_cases[55]],
        ]
        assert data.dataloader_valid.dataset.y.tolist() == [
            [normalised_cases[550 - 450]],
            [normalised_cases[650 - 550]],
            [normalised_cases[55 - 45]],
            [normalised_cases[65 - 55]],
        ]
