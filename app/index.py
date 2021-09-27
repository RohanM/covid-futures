import json
from flask import Blueprint
from flask import render_template

from app.lib.models import Case

bp = Blueprint('index', __name__)

@bp.route("/")
def index():
    states = Case.states()
    state_data = {}

    for state in states:
        state_data[state] = []
        cases = Case.query.filter(Case.state == state).order_by(Case.date.asc()).all()
        labels = list(map(lambda case: case.date.strftime('%Y-%m-%d'), cases))
        values = list(map(lambda case: case.confirmed, cases))
        state_data[state].append({'name': 'Cases', 'labels': labels, 'values': values})

    return render_template(
        'index.html',
        states=state_data,
        max_confirmed=Case.max_confirmed()
    )
