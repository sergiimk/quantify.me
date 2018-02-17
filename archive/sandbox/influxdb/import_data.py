import sys
sys.path.insert(0, '../../utils/src')

import json
from influxdb import client as influxdb
from utils import iso8601

db = influxdb.InfluxDBClient('boot2docker', 8086, 'root', 'root', 'quantify')

with open(sys.argv[1]) as f:
    js = json.load(f)

for e in js:
	if 'delta' in e:
		e['delta'] = float(e['delta'].replace(',', ''))

series = sys.argv[2]

columns = {k for e in js for k in e}
columns.remove('t')
columns.remove('type')
columns = list(columns)
columns.sort()
columns.insert(0, 'time')

points = [
    [
        iso8601.to_utc_timestamp(iso8601.parse(e['t'])),
    ] + [
        e.get(c, '')
        for c in columns[1:]
    ]
    for e in js
]

data = [{
    'name': series,
    'points': points,
    'columns': columns
}]

db.write_points(data)