import json
from flask import Blueprint
from flask import render_template

from sqlalchemy.sql import functions as func

from app import db
from app.lib.models import Case

bp = Blueprint('index', __name__)

@bp.route("/")
def index():
    states = get_states()
    state_data = {}

    for state in states:
        cases = Case.query.filter(Case.state == state).order_by(Case.date.asc()).all()
        labels = list(map(lambda case: case.date.strftime('%Y-%m-%d'), cases))
        values = list(map(lambda case: case.confirmed, cases))
        state_data[state] = (labels, values)

    return render_template(
        'index.html',
        states=state_data
    )

def get_states():
    """Get all states, those with the most total cases first"""
    states = db.session.query(Case.state).group_by(Case.state).order_by(func.sum(Case.confirmed).desc()).all()
    return [state[0] for state in states]
