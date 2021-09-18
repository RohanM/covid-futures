import pytest

from app import create_app, db
from app.lib.models import Case

@pytest.fixture
def app(): return create_app(True)

@pytest.fixture
def database(app):
    db.create_all()
    Case.query.delete()
    return db
