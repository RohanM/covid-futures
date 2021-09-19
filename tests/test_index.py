import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def index(client):
    rv = client.get('/')
    return BeautifulSoup(rv.data, 'html.parser')


def test_title(index):
    assert index.select('h2')[0].string == 'COVID Futures'

def test_graph_data(db_seeds, index):
    db_seeds
    assert index.select('#graph-vic')[0]['data-labels'] == "['2021-09-01', '2021-09-02', '2021-09-03']"
    assert index.select('#graph-vic')[0]['data-values'] == "[10, 20, 30]"
