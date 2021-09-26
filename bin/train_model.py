#!/usr/bin/env python3

from app import create_app, db

from app.lib.ml_model import MLModel
from app.lib.ml_model_data import MLModelData

epochs = 500

with create_app().app_context():
    data = MLModelData(input_window=30, output_window=30, train_valid_split=0.8)
    data.load()
    model = MLModel(input_window=30, output_window=30, data_mean=data.mean, data_std=data.std)
    train_losses, valid_losses = model.fit(epochs, data.dataloader_train, data.dataloader_valid)
    model.save('./model.pt')
