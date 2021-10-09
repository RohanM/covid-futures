import pytest
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SequentialSampler, RandomSampler
from app.lib.dataset import Dataset
from app.lib.data_pipeline import BuildDataloaders

@pytest.fixture
def dls():
    data = {
        'all_train': Dataset([10], [20]),
        'all_valid': Dataset([20], [30]),
    }
    return BuildDataloaders({
        'all_train': { 'batch_size': 64, 'shuffle': True },
        'all_valid': { 'batch_size': 64, 'shuffle': False },
    }).perform(data)

@pytest.fixture
def empty_dls():
    data = {
        'all_train': Dataset([], []),
        'all_valid': Dataset([], []),
    }
    return BuildDataloaders({
        'all_train': { 'batch_size': 64, 'shuffle': True },
        'all_valid': { 'batch_size': 64, 'shuffle': False },
    }).perform(data)


def test_data(dls):
    assert dls['all_train'].dataset == Dataset([10], [20])
    assert dls['all_valid'].dataset == Dataset([20], [30])

def test_batch_size(dls):
    assert dls['all_train'].batch_size == 64
    assert dls['all_valid'].batch_size == 64

def test_shuffle(dls):
    assert isinstance(dls['all_train'].sampler, RandomSampler)
    assert isinstance(dls['all_valid'].sampler, SequentialSampler)

def test_empty_data(empty_dls):
    assert empty_dls['all_train'] == None
    assert empty_dls['all_valid'] == None
