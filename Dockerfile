FROM ubuntu:13.10

RUN sudo apt-get update
RUN sudo apt-get install -qy python3-setuptools
RUN sudo easy_install3 pip

RUN sudo apt-get install -qy nginx
ADD nginx.conf /etc/nginx/nginx.conf

ADD requirements.txt /quantify/requirements.txt
RUN pip install --upgrade -r /quantify/requirements.txt

ADD . /quantify

EXPOSE 8080
WORKDIR /quantify/api
ENV PYTHONPATH /quantify/tsdb
CMD ["python3", "api.py"]
