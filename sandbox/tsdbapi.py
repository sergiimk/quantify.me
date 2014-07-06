from flask import Flask, request, Response, jsonify
import http.client
import sqlite3
import contextlib
import iso8601
import json


app = Flask(__name__)

@contextlib.contextmanager
def transaction():
    db = sqlite3.connect('tsdb.db')
    try:
        with db:
            yield db
    finally:
        db.close()


@app.route('/sensor/<int:sensor_id>', methods=['GET'])
def get_data(sensor_id):
    with transaction() as tr:
        cur = tr.cursor()
        cur.execute('SELECT data FROM events WHERE sensor_id=?',
                    (sensor_id,))

        data = list(map(lambda r: json.loads(r[0]),
                        cur.fetchall()))

        return jsonify(data=data)


@app.route('/sensor/<int:sensor_id>', methods=['PUT', 'POST'])
def set_data(sensor_id):
    with transaction() as tr:

        if request.method == 'PUT':
            tr.execute('DELETE FROM events WHERE sensor_id=?',
                       (sensor_id,))

        for event in request.json:
            ts = iso8601.to_utc_timestamp(iso8601.parse(event['t']))
            data = json.dumps(event)

            tr.execute(
                'INSERT INTO events (sensor_id, ts, data) VALUES(?, ?, ?)',
                (sensor_id, ts, data))

        return Response(status=http.client.CREATED)


if __name__ == '__main__':
    db = sqlite3.connect('tsdb.db')
    db.execute('CREATE TABLE IF NOT EXISTS events (sensor_id, ts, data)')
    app.run('0.0.0.0', 8080, debug=True)