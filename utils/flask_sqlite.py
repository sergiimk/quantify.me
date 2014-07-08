import sqlite3
from flask import current_app
from flask import _app_ctx_stack as stack


class SQLite3(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def connect(self):
        return sqlite3.connect(current_app.config['DATABASE'])

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, '_db'):
            ctx._db.close()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, '_db'):
                ctx._db = self.connect()
            return ctx._db