import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def index(client):
    rv = client.get('/')
    return BeautifulSoup(rv.data, 'html.parser')


def test_graph_data(db_simple_cases, index):
    assert index.select('#graph-vic')[0]['data-labels'] == '["2021-09-01", "2021-09-02", "2021-09-03"]'
    assert index.select('#graph-vic')[0]['data-values'] == "[10, 20, 30]"
    assert index.select('#graph-nsw')[0]['data-labels'] == '["2021-09-01", "2021-09-02", "2021-09-03"]'
    assert index.select('#graph-nsw')[0]['data-values'] == "[100, 200, 300]"

def test_ordered_by_total_cases(db_simple_cases, index):
    assert list(map(lambda graph: graph['id'], index.select('.graph'))) == ['graph-nsw', 'graph-vic']

def test_consistent_y_axis(db_simple_cases, index):
    assert index.select('#graph-vic')[0]['data-max-y'] == '300'
    assert index.select('#graph-nsw')[0]['data-max-y'] == '300'
