#!/bin/sh

docker run \
  -p 80:80 \
  --name=quantify_web \
  -v $PWD/src:/quantify/web \
  -i -t \
  --rm=true \
  quantify_web
