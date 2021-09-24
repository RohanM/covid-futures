from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import functions as func
from app import db

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    state = db.Column(db.String(10), nullable=False)
    confirmed = db.Column(db.Integer)

    __table_args__ = (
        UniqueConstraint('date', 'state', name='uq_cases_date_state'),
    )

    @staticmethod
    def states():
        """Get all states, those with the most total cases first"""
        states = db.session.query(Case.state).group_by(Case.state).order_by(func.sum(Case.confirmed).desc()).all()
        return [state[0] for state in states]

    @staticmethod
    def max_confirmed():
        """Returns the maximum confirmed cases on any one day"""
        return db.session.query(func.max(Case.confirmed)).scalar()


    def as_dict(self):
        return { k:v for k,v in self.__dict__.items() if k in Case.__table__.columns.keys() }

    def __repr(self):
        return '<Case %d>' % id
