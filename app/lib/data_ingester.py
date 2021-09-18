import io
import datetime
import requests
import csv
from app import db
from app.lib.models import Case

class DataIngester:
    URL = "https://github.com/M3IT/COVID-19_Data/raw/master/Data/COVID_AU_state.csv"

    def ingest(self):
        for row in self.csv_reader():
            self.upsert_row(row)
        db.session.commit()

    def upsert_row(self, row):
        case = Case(
            date=datetime.datetime.strptime(row['date'], '%Y-%m-%d'),
            state=row['state_abbrev'],
            confirmed=row['confirmed']
        )
        db.session.add(case)

    def csv_reader(self):
        return csv.DictReader(self.csv_data())

    def csv_data(self):
        page = requests.get(self.URL)
        return io.StringIO(page.content.decode())
