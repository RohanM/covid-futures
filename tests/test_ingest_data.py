import pytest
import requests_mock
import datetime

from app.lib.models import Case
from app.lib.data_ingester import DataIngester

@pytest.fixture
def mock_covid_au_state_csv(requests_mock):
    with open('./tests/data/COVID_AU_state.csv') as mock_csv:
        requests_mock.get(
            'https://github.com/M3IT/COVID-19_Data/raw/master/Data/COVID_AU_state.csv',
            text=mock_csv.read()
        )

@pytest.fixture
def ingester():
    return DataIngester()

def test_ingest(app, database, mock_covid_au_state_csv, ingester):
    with app.app_context():
        ingester.ingest()
        assert Case.query.count() == 4816

def test_ingest_data(app, database, mock_covid_au_state_csv, ingester):
    with app.app_context():
        ingester.ingest()
        case = Case.query.first()
        assert case.date == datetime.date(2020, 1, 25)
        assert case.state == 'ACT'
        assert case.confirmed == 0
