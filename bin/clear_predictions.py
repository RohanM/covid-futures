#!/usr/bin/env python3

from app import create_app, db
from app.lib.models import Case, Prediction, PredictionData

with create_app().app_context():
    PredictionData.query.delete()
    Prediction.query.delete()
    db.session.commit()
