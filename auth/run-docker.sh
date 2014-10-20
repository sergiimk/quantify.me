#!/bin/sh

docker run \
  -p 8080:8080 \
  --name quantify_auth \
  -v $PWD/../utils/src/utils:/quantify/utils \
  --rm=true \
  -i -t \
  quantify_auth
