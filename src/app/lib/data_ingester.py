import io
import datetime
import requests
import csv
from app import db
from app.lib.models import Case

class DataIngester:
    URL = "https://github.com/M3IT/COVID-19_Data/raw/master/Data/COVID_AU_state.csv"

    def ingest(self):
        cases = []
        for row in self.csv_reader():
            cases.append(self.case_for_row(row).as_dict())
        self.bulk_insert_cases(cases)

    def bulk_insert_cases(self, cases):
        """Insert cases with MySQL INSERT IGNORE syntax, which ignores duplicate rows"""
        insert = Case.__table__.insert().prefix_with(' IGNORE').values(cases)
        db.session.execute(insert)
        db.session.commit()

    def case_for_row(self, row):
        return Case(
            date=datetime.datetime.strptime(row['date'], '%Y-%m-%d'),
            state=row['state_abbrev'],
            confirmed=row['confirmed']
        )

    def csv_reader(self):
        return csv.DictReader(self.csv_data())

    def csv_data(self):
        page = requests.get(self.URL)
        return io.StringIO(page.content.decode())
