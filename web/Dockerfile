FROM ubuntu:13.10

RUN apt-get update
RUN apt-get install -qy nginx
ADD nginx.conf /etc/nginx/nginx.conf

ADD src /quantify/web

EXPOSE 80
WORKDIR /quantify
CMD nginx
