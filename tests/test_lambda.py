import pytest

from app.lib.lambda_layer import Lambda

def test_lambda():
    l = Lambda(lambda x: x * 2)
    assert l.forward(5) == 10
