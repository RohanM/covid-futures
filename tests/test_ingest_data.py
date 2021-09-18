import pytest

from app.lib.data_ingester import DataIngester

@pytest.fixture
def ingester():
    return DataIngester()

def test_ingest(ingester):
    assert ingester.ingest()
