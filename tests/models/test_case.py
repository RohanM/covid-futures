import pytest
import datetime

from app.lib.models import Case

def test_confirmed_for_state(app, db_simple_cases):
    with app.app_context():
        assert Case.confirmed_for_state('VIC') == [10, 20, 30]
        assert Case.confirmed_for_state('NSW') == [100, 200, 300]

def test_states(app, db_simple_cases):
    with app.app_context():
        assert Case.states() == ['NSW', 'VIC']

def test_max_confirmed(app, db_simple_cases):
    with app.app_context():
        assert Case.max_confirmed() == 300

def test_case_as_dict():
    case = Case(date=datetime.date(2021, 9, 1), state='VIC', confirmed=10)
    assert case.as_dict() == {
        'date': datetime.date(2021, 9, 1),
        'state': 'VIC',
        'confirmed': 10,
    }
