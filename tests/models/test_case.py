import pytest
import datetime

from app.lib.models import Case

def test_case_as_dict():
    case = Case(date=datetime.date(2021, 9, 1), state='VIC', confirmed=10)
    assert case.as_dict() == {
        'date': datetime.date(2021, 9, 1),
        'state': 'VIC',
        'confirmed': 10,
    }
