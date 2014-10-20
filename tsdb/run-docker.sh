#!/bin/sh

docker run \
  -p 8081:8080 \
  --name quantify_tsdb \
  -v $PWD/../utils/src/utils:/quantify/utils \
  --rm=true \
  -i -t \
  quantify_tsdb
