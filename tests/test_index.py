import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def index(client):
    rv = client.get('/')
    return BeautifulSoup(rv.data, 'html.parser')


def test_graph_data(db_extended_cases, index):
    assert index.select('#graph-vic')[0]['data-series'] == '[{"labels": ["2021-09-07"], "name": "Cases", "values": [39.99999999999999]}]'
    assert index.select('#graph-nsw')[0]['data-series'] == '[{"labels": ["2021-09-07"], "name": "Cases", "values": [400.0]}]'

def test_graph_predictions(db_simple_cases, db_predictions, index):
    assert '{"labels": ["2021-09-01", "2021-09-02", "2021-09-03"], "name": "Prediction 01-09-2021", "values": [1, 2, 3]}' in index.select('#graph-vic')[0]['data-series']
    assert '{"labels": ["2021-09-01", "2021-09-02", "2021-09-03"], "name": "Prediction 01-09-2021", "values": [10, 20, 30]}' in index.select('#graph-nsw')[0]['data-series']

def test_ordered_by_total_cases(db_simple_cases, index):
    assert list(map(lambda graph: graph['id'], index.select('.graph'))) == ['graph-nsw', 'graph-vic']

def test_consistent_y_axis(db_simple_cases, index):
    assert index.select('#graph-vic')[0]['data-max-y'] == '300'
    assert index.select('#graph-nsw')[0]['data-max-y'] == '300'
