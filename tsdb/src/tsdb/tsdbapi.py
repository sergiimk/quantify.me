from flask import Flask, request, Response, json
from flask_cors import cross_origin
from tsdb.models import db, Event
import http.client
from utils import iso8601

TIME_FMT_HEADER = 'Event-Time-Format'
TIME_FMT_DEFAULT = 'iso8601'

app = Flask(__name__)

#TODO: separate web API layer, remove CORS
#TODO: fix CORS method composition


def json_to_event(sensor_id, event_data):
    ts = iso8601.to_utc_timestamp(iso8601.parse(event_data['t']))
    data = json.dumps(event_data)

    return Event(
        sensor_id=sensor_id,
        ts=ts,
        data=data
    )


def event_to_json(event):
    event_time_fmt = request.headers.get(
        TIME_FMT_HEADER, TIME_FMT_DEFAULT
    ).lower().split(',')

    event_data = json.loads(event.data)
    t = event_data.pop('t')

    if 'unix' in event_time_fmt:
        event_data['ts'] = str(
            iso8601.to_utc_timestamp(
                iso8601.parse(t)
            )
        )

    if 'iso8601' in event_time_fmt:
        event_data['t'] = t

    return event_data


@app.route('/sensors/<int:sensor_id>', methods=['GET'])
@cross_origin(
    headers=['Content-Type', TIME_FMT_HEADER],
    methods=['HEAD', 'GET', 'PUT', 'POST', 'DELETE'],
)
def get_data(sensor_id):
    raw_events = db.session.query(Event).filter(
        Event.sensor_id == sensor_id
    ).all()

    data = [event_to_json(e) for e in raw_events]

    return Response(json.dumps(data), mimetype='application/json')


@app.route('/sensors/<int:sensor_id>', methods=['PUT', 'POST'])
@cross_origin(
    headers='Content-Type',
    methods=['HEAD', 'GET', 'PUT', 'POST', 'DELETE'],
)
def set_data(sensor_id):
    if request.method == 'PUT':
        db.session.query(Event).filter(
            Event.sensor_id == sensor_id
        ).delete()

    for event_data in request.json:
        db.session.add(json_to_event(sensor_id, event_data))

    db.session.commit()

    return Response(status=http.client.CREATED)


@app.route('/sensors/<int:sensor_id>/file', methods=['GET'])
@cross_origin(headers=['Content-Type', TIME_FMT_HEADER])
def get_data_file(sensor_id):
    response = get_data(sensor_id)
    response.headers['Content-Disposition'] = \
        'attachment; filename=sensor_{}.json'.format(sensor_id)
    return response


@app.route('/sensors/<int:sensor_id>/file', methods=['POST'])
@cross_origin(headers='Content-Type')
def set_data_file(sensor_id):
    db.session.query(Event).filter(
        Event.sensor_id == sensor_id
    ).delete()

    for f in request.files.values():
        events_data = json.load(f)
        for event_data in events_data:
            db.session.add(json_to_event(sensor_id, event_data))

    db.session.commit()

    return Response(status=http.client.CREATED)


@app.route('/sensors/<int:sensor_id>', methods=['DELETE'])
@cross_origin(
    headers='Content-Type',
    methods=['HEAD', 'GET', 'PUT', 'POST', 'DELETE'],
)
def delete_data(sensor_id):
    db.session.query(Event).filter(
        Event.sensor_id == sensor_id
    ).delete()

    db.session.commit()

    return Response(status=http.client.OK)


if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    db.app = app
    db.create_all()
    app.run('0.0.0.0', 8080, debug=True)
