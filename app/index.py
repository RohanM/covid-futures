import json
from flask import Blueprint
from flask import render_template

from app.lib.models import Case

bp = Blueprint('index', __name__)

@bp.route("/")
def index():
    cases = Case.query.filter(Case.state == 'VIC').order_by(Case.date.asc()).all()
    labels = list(map(lambda case: case.date.strftime('%Y-%m-%d'), cases))
    values = list(map(lambda case: case.confirmed, cases))

    return render_template(
        'index.html',
        labels=json.dumps(labels),
        values=json.dumps(values)
    )
