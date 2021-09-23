from sqlalchemy import UniqueConstraint
from app import db

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    state = db.Column(db.String(10), nullable=False)
    confirmed = db.Column(db.Integer)

    __table_args__ = (
        UniqueConstraint('date', 'state', name='uq_cases_date_state'),
    )

    def __repr(self):
        return '<Case %d>' % id
