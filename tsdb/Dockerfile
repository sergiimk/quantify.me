FROM ubuntu:13.10

RUN apt-get update
RUN apt-get install -qy python3-setuptools
RUN easy_install3 pip

ADD requirements.txt /quantify/tsdb/requirements.txt
RUN pip install --upgrade -r /quantify/tsdb/requirements.txt

ADD src/tsdb /quantify/tsdb
# TODO: add utils dependency

EXPOSE 8080
WORKDIR /quantify
ENV PYTHONPATH /quantify
CMD ["python3", "tsdb/tsdbapi.py"]
