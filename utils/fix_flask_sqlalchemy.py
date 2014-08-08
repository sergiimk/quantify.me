"""
Fixes in-memory db issue with flask-sqlalchemy
https://github.com/mitsuhiko/flask-sqlalchemy/pull/81
"""
from flask.ext.sqlalchemy import SQLAlchemy as SQLAlchemyOrig
from sqlalchemy.pool import StaticPool


class SQLAlchemy(SQLAlchemyOrig):
    def apply_driver_hacks(self, app, info, options):
        options['poolclass'] = StaticPool
        options['connect_args'] = {'check_same_thread': False}
        return super().apply_driver_hacks(app, info, options)
