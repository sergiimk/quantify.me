#!/bin/bash
docker run \
    -t \
    -i \
    --rm \
    -p 80:80 \
    -e INFLUXDB_HOST=boot2docker \
    -e INFLUXDB_PORT=8086 \
    -e INFLUXDB_NAME=quantify \
    -e INFLUXDB_USER=root \
    -e INFLUXDB_PASS=root \
    -e INFLUXDB_IS_GRAFANADB=true \
    -e HTTP_USER=test \
    -e HTTP_PASS=test \
    tutum/grafana
