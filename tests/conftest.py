import pytest
import datetime

from app import create_app, db
from app.lib.models import Case, Prediction, PredictionData

@pytest.fixture
def app(): return create_app(True)

@pytest.fixture
def database(app):
    db.create_all()
    Case.query.delete()
    PredictionData.query.delete()
    Prediction.query.delete()
    return db

@pytest.fixture
def db_simple_cases(database):
    db.session.add(Case(date=datetime.date(2021, 9, 1), state='VIC', confirmed=10))
    db.session.add(Case(date=datetime.date(2021, 9, 2), state='VIC', confirmed=20))
    db.session.add(Case(date=datetime.date(2021, 9, 3), state='VIC', confirmed=30))
    db.session.add(Case(date=datetime.date(2021, 9, 1), state='NSW', confirmed=100))
    db.session.add(Case(date=datetime.date(2021, 9, 2), state='NSW', confirmed=200))
    db.session.add(Case(date=datetime.date(2021, 9, 3), state='NSW', confirmed=300))
    db.session.commit()

@pytest.fixture
def db_extended_cases(database, db_simple_cases):
    db.session.add(Case(date=datetime.date(2021, 9, 4), state='VIC', confirmed=40))
    db.session.add(Case(date=datetime.date(2021, 9, 5), state='VIC', confirmed=50))
    db.session.add(Case(date=datetime.date(2021, 9, 6), state='VIC', confirmed=60))
    db.session.add(Case(date=datetime.date(2021, 9, 7), state='VIC', confirmed=70))
    db.session.add(Case(date=datetime.date(2021, 9, 4), state='NSW', confirmed=400))
    db.session.add(Case(date=datetime.date(2021, 9, 5), state='NSW', confirmed=500))
    db.session.add(Case(date=datetime.date(2021, 9, 6), state='NSW', confirmed=600))
    db.session.add(Case(date=datetime.date(2021, 9, 7), state='NSW', confirmed=700))
    db.session.commit()

@pytest.fixture
def db_predictions(database):
    Prediction.save_sequence('VIC', datetime.date(2021, 9, 1), [1, 2, 3])
    Prediction.save_sequence('NSW', datetime.date(2021, 9, 1), [10, 20, 30])
