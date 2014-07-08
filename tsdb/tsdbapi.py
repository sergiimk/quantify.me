from flask import Flask, request, Response, jsonify, json
from flask_sqlite import SQLite3
import http.client
import iso8601


app = Flask(__name__)
db = SQLite3(app)


def init_db(conn):
    conn.execute(
        'CREATE TABLE IF NOT EXISTS events '
        '(sensor_id, ts, data)')


@app.route('/sensors/<int:sensor_id>', methods=['GET'])
def get_data(sensor_id):
    with db.connection as tr:
        cur = tr.cursor()
        cur.execute('SELECT data FROM events '
                    'WHERE sensor_id=?', (sensor_id,))

        data = list(map(lambda r: json.loads(r[0]),
                        cur.fetchall()))

        return jsonify(data=data)


@app.route('/sensors/<int:sensor_id>', methods=['PUT', 'POST'])
def set_data(sensor_id):
    with db.connection as tr:
        if request.method == 'PUT':
            tr.execute('DELETE FROM events '
                       'WHERE sensor_id=?', (sensor_id,))

        for event in request.json:
            ts = iso8601.to_utc_timestamp(iso8601.parse(event['t']))
            data = json.dumps(event)

            tr.execute(
                'INSERT INTO events (sensor_id, ts, data) '
                'VALUES(?, ?, ?)', (sensor_id, ts, data))

        return Response(status=http.client.CREATED)


if __name__ == '__main__':
    import sqlite3
    cs = 'file:tsdb?mode=memory&cache=shared'
    memdb = sqlite3.connect(cs)
    init_db(memdb)

    app.config.setdefault('DATABASE', cs)
    app.run('0.0.0.0', 8081, debug=True)