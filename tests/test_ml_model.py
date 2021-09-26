import pytest
from app.lib.ml_model import MLModel
from app.lib.ml_model_data import MLModelData

def test_fit(app, db_extended_cases):
    """Integration test of MLModelData with MLModel.fit()"""
    with app.app_context():
        data = MLModelData(input_window=2, output_window=2, train_valid_split=0.75)
        data.load()
        model = MLModel(input_window=2, output_window=2)
        train_losses, valid_losses = model.fit(2, data.dataloader_train, data.dataloader_valid)
        assert len(train_losses) == 2
        assert len(valid_losses) == 2

def test_predict():
    model = MLModel(input_window=2, output_window=2)
    prediction = model.predict([1, 2])
    assert len(prediction) == 2

def test_save_load():
    model = MLModel(input_window=2, output_window=2)
    model.save('./tests/model.pt')
    model.load('./tests/model.pt')
