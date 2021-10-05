import json
from flask import Blueprint
from flask import render_template

from app.lib import running_mean
from app.lib.models import Case, Prediction, PredictionData

bp = Blueprint('index', __name__)

@bp.route("/")
def index():
    states = Case.states()
    state_data = {}

    for state in states:
        state_data[state] = []
        state_data[state].append(build_state_cases(state))
        for prediction in build_state_predictions(state):
            state_data[state].append(prediction)

    return render_template(
        'index.html',
        states=state_data,
        max_confirmed=Case.max_confirmed()
    )

def build_state_cases(state):
    cases = Case.query.filter(Case.state == state).order_by(Case.date.asc()).all()
    labels = list(map(lambda case: case.date.strftime('%Y-%m-%d'), cases))[6:]
    values = list(running_mean(list(map(lambda case: case.confirmed, cases))))
    return {'name': 'Cases', 'labels': labels, 'values': values}

def build_state_predictions(state):
    predictions = Prediction.query.filter_by(state=state).all()
    return [build_prediction(prediction) for prediction in predictions]

def build_prediction(prediction):
    labels = list(map(lambda d: d.date.strftime('%Y-%m-%d'), prediction.data))
    values = list(map(lambda d: d.confirmed, prediction.data))
    return {
        'name': f'Prediction {prediction.name}',
        'labels': labels,
        'values': values
    }
