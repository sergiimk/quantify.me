from tsdb.file import TSDBFile
from tsdb.streams import JsonStream, isodates
from flask import Flask, Response, request
from flaskx import crossdomain
from flask_negotiate import consumes, produces
import io
import itertools


app = Flask(__name__)
db = TSDBFile.open('../res/db.json')


def yield_json(events):
    ss = io.StringIO()
    js = JsonStream(ss)
    js.write_start()
    for e in events:
        js.write(e)
        yield ss.getvalue()
        ss.seek(0)
        ss.truncate()
    js.write_end()
    yield ss.getvalue()


def map_duration(events):
    prev = None
    for curr in itertools.chain(events, [{'t': isodates.utcnow()}]):
        if prev is not None:
            prev['duration'] = (curr['t'] - prev['t']).total_seconds()
            yield prev
        prev = curr


@app.route('/', methods=['GET'])
@crossdomain('*')
#@produces('application/json') # TODO: flask-negotiate bug
def index():
    return Response(
        yield_json(map_duration(db.read())),
        content_type='application/json')


@app.route('/', methods=['POST'])
@consumes('application/json')
def write():
    for e in request.json:
        e['t'] = isodates.parse(e['t'])
        db.append(e)
    return Response(status=204)


if __name__ == '__main__':
    with db:
        app.run(host='0.0.0.0', port=8080, debug=True)
