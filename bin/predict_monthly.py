#!/usr/bin/env python3

import datetime
from app import create_app
from app.lib.models import Case, Prediction, PredictionData
from app.lib.ml_model import MLModel
from app.lib.ml_model_data import MLModelData

input_window = 30
output_window = 30

with create_app().app_context():
    data = MLModelData(input_window=input_window, output_window=output_window)
    data.load()
    model = MLModel(input_window=input_window, output_window=output_window)
    model.load('./model.pt')

    for state in Case.states():
        # We start a month in (to provide enough data for our input window)
        first_date = Case.earliest_date(state) + datetime.timedelta(days=input_window)
        num_days = (Case.latest_date(state) - first_date).days

        for day in range(0, num_days, 30):
            prediction_date = first_date + datetime.timedelta(days=day)
            cases = data.data[state][day:day+input_window]
            prediction_data = model.predict(cases).int().tolist()
            Prediction.save_sequence(state, prediction_date, prediction_data)
