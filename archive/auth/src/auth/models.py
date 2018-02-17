from utils.fix_flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, unique=True)
    password = db.Column(db.String(256))
