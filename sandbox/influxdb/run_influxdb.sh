#!/bin/bash
docker run \
    -t \
    -i \
    --rm \
    -p 8083:8083 \
    -p 8086:8086 \
    -e PRE_CREATE_DB="quantify" \
    tutum/influxdb:latest

