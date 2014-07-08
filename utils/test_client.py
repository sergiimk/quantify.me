from flask.testing import FlaskClient
from flask import json


class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        data = kwargs.pop('data', None)
        content_type = kwargs.pop('content_type', None)

        if isinstance(data, (dict, list)):
            data = json.dumps(data)
            if not content_type:
                content_type = 'application/json'

        resp = super().open(
            *args,
            content_type=content_type,
            data=data,
            **kwargs)

        if resp.content_type == 'application/json':
            resp.json = json.loads(resp.data)

        return resp
