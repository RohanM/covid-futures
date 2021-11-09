import pytest
import datetime

from app.lib.models import Prediction, PredictionData

def test_save_sequence(app, database):
    with app.app_context():
        state = 'VIC'
        date = datetime.date(2021, 9, 26)
        data = [1, 2, 3]
        Prediction.save_sequence(state, date, data)

        prediction = Prediction.query.filter_by(name='26-09-2021', state=state).first()
        data = PredictionData.query.filter_by(prediction_id=prediction.id).order_by(PredictionData.date).all()
        assert [(p.date, p.confirmed) for p in data] == [
            (datetime.date(2021, 9, 26), 1),
            (datetime.date(2021, 9, 27), 2),
            (datetime.date(2021, 9, 28), 3),
        ]
