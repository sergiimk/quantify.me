FROM ubuntu:13.10

RUN apt-get update
RUN apt-get install -qy python3-setuptools
RUN easy_install3 pip

ADD requirements.txt /quantify/requirements.txt
RUN pip install --upgrade -r /quantify/requirements.txt

ADD . /quantify

EXPOSE 8081
WORKDIR /quantify/sandbox
ENV PYTHONPATH /quantify/sandbox
CMD ["python3", "accounts.py"]
