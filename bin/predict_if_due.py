#!/usr/bin/env python3

import datetime
from app import create_app
from app.lib.models import Case, Prediction, PredictionData
from app.lib.ml_model import MLModel
from app.lib.ml_model_data import MLModelData

input_window = 30
output_window = 30

with create_app().app_context():
    if datetime.date.today() > PredictionData.latest_date():
        data = MLModelData(input_window=input_window, output_window=output_window)
        data.load()
        model = MLModel(input_window=input_window, output_window=output_window)
        model.load('./model.pt')

        for state in Case.states():
            prediction_date = Case.latest_date(state) + datetime.timedelta(days=1)
            recent_cases = data.data[state][-input_window:]
            prediction_data = model.predict(recent_cases).int().tolist()
            Prediction.save_sequence(state, prediction_date, prediction_data)
