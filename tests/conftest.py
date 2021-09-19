import pytest
import datetime

from app import create_app, db
from app.lib.models import Case

@pytest.fixture
def app(): return create_app(True)

@pytest.fixture
def database(app):
    db.create_all()
    Case.query.delete()
    return db

@pytest.fixture
def db_seeds(database):
    db.session.add(Case(date=datetime.date(2021, 9, 1), state='VIC', confirmed=10))
    db.session.add(Case(date=datetime.date(2021, 9, 2), state='VIC', confirmed=20))
    db.session.add(Case(date=datetime.date(2021, 9, 3), state='VIC', confirmed=30))
    db.session.add(Case(date=datetime.date(2021, 9, 1), state='NSW', confirmed=100))
    db.session.add(Case(date=datetime.date(2021, 9, 2), state='NSW', confirmed=200))
    db.session.add(Case(date=datetime.date(2021, 9, 3), state='NSW', confirmed=300))
    db.session.commit()
