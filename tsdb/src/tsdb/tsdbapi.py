from flask import Flask, request, Response, json
from utils.flask_sqlite import SQLite3
from flask_cors import cross_origin
import http.client
from utils import iso8601


app = Flask(__name__)
db = SQLite3(app)

#TODO: separate web API layer, remove CORS
#TODO: fix CORS method composition


def init_db(conn):
    conn.execute(
        'CREATE TABLE IF NOT EXISTS events '
        '(sensor_id, ts, data)')


@app.route('/sensors/<int:sensor_id>', methods=['GET'])
@cross_origin(headers='Content-Type', methods=['HEAD', 'GET', 'PUT', 'POST', 'DELETE'])
def get_data(sensor_id):
    with db.connection as tr:
        cur = tr.cursor()
        cur.execute('SELECT data FROM events '
                    'WHERE sensor_id=?', (sensor_id,))

        data = list(map(lambda r: json.loads(r[0]),
                        cur.fetchall()))

        return Response(json.dumps(data),
                        mimetype='application/json')


@app.route('/sensors/<int:sensor_id>/file', methods=['GET'])
@cross_origin(headers='Content-Type')
def get_data_file(sensor_id):
    response = get_data(sensor_id)
    response.headers['Content-Disposition'] = \
        'attachment; filename=sensor_{}.json'.format(sensor_id)
    return response


@app.route('/sensors/<int:sensor_id>', methods=['PUT', 'POST'])
@cross_origin(headers='Content-Type', methods=['HEAD', 'GET', 'PUT', 'POST', 'DELETE'])
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


@app.route('/sensors/<int:sensor_id>/file', methods=['POST'])
@cross_origin(headers='Content-Type')
def set_data_file(sensor_id):
    print(request.files)
    return Response(status=http.client.CREATED)


@app.route('/sensors/<int:sensor_id>', methods=['DELETE'])
@cross_origin(headers='Content-Type', methods=['HEAD', 'GET', 'PUT', 'POST', 'DELETE'])
def delete_data(sensor_id):
    with db.connection as tr:
        tr.execute('DELETE FROM events '
                   'WHERE sensor_id=?', (sensor_id,))
    return Response(status=http.client.OK)


if __name__ == '__main__':
    import sqlite3
    cs = 'file:tsdb?mode=memory&cache=shared'
    memdb = sqlite3.connect(cs)
    init_db(memdb)

    app.config.setdefault('DATABASE', cs)
    app.run('0.0.0.0', 8080, debug=True)