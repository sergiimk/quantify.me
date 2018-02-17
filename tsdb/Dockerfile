FROM ubuntu:17.04

RUN apt-get update
RUN apt-get install -qy python3.6 wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py

ADD requirements.txt /quantify/tsdb/requirements.txt
RUN pip install --upgrade -r /quantify/tsdb/requirements.txt

ADD src/tsdb /quantify/tsdb
# TODO: add utils dependency

EXPOSE 8080
WORKDIR /quantify
ENV PYTHONPATH /quantify
CMD ["python3.6", "tsdb/tsdbapi.py"]
