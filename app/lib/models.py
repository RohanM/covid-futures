import datetime
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
    def confirmed_for_state(state):
        cases = Case.query.with_entities(Case.confirmed).filter(Case.state == state).order_by(Case.date.asc()).all()
        return [case[0] for case in cases]

    @staticmethod
    def states():
        """Get all states, those with the most total cases first"""
        states = db.session.query(Case.state).group_by(Case.state).order_by(func.sum(Case.confirmed).desc()).all()
        return [state[0] for state in states]

    @staticmethod
    def max_confirmed():
        """Returns the maximum confirmed cases on any one day"""
        return db.session.query(func.max(Case.confirmed)).scalar()

    @staticmethod
    def earliest_date(state):
        """Returns the earliest date we have data for the specified state"""
        return db.session.query(Case.date).order_by(Case.date.asc()).limit(1).scalar()

    @staticmethod
    def latest_date(state):
        """Returns the most recent date we have data for the specified state"""
        return db.session.query(Case.date).order_by(Case.date.desc()).limit(1).scalar()

    def as_dict(self):
        return { k:v for k,v in self.__dict__.items() if k in Case.__table__.columns.keys() }

    def __repr(self):
        return '<Case %d>' % id


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(10), nullable=False)

    data = db.relationship('PredictionData', back_populates='prediction')

    __table_args__ = (
        UniqueConstraint('name', 'state', name='uq_predictions_name_state'),
    )

    @staticmethod
    def save(state, date, data):
        name = date.strftime('%d-%m-%Y')
        prediction = Prediction(name=name, state=state)
        db.session.add(prediction)
        db.session.commit()

        for i in range(len(data)):
            db.session.add(
                PredictionData(
                    prediction_id=prediction.id,
                    date=date + datetime.timedelta(days=i),
                    confirmed=data[i],
                )
            )
        db.session.commit()


class PredictionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('prediction.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    confirmed = db.Column(db.Integer, nullable=False)

    prediction = db.relationship('Prediction', back_populates='data')

    __table_args__ = (
        UniqueConstraint('prediction_id', 'date', name='uq_prediction_data_prediction_id_date'),
    )
