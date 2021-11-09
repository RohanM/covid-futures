#!/usr/bin/env python3

# Usage: python load_csv.py <prediction name> <state> <csv file>

import sys
import csv
import datetime

from app import create_app
from app.lib.models import Prediction


def load_cases(filename):
    cases = []
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            cases.append((
                datetime.datetime.strptime(row[0], '%Y/%m/%d'),
                round(float(row[1])),
            ))
    return cases


if len(sys.argv) <= 3:
    print('Usage: python load_csv.py <prediction name> <state> <csv file>')
    exit(1)

prediction_name = sys.argv[1]
state = sys.argv[2]
filename = sys.argv[3]

cases = load_cases(filename)

with create_app().app_context():
    Prediction.save_scatter(name=prediction_name, state=state, data=cases)
