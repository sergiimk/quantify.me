from utils.fix_flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer())
    ts = db.Column(db.String(256))
    data = db.Column(db.Text())
