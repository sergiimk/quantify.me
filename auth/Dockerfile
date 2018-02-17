FROM ubuntu:17.04

RUN apt-get update
RUN apt-get install -qy python3.6 wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py

ADD requirements.txt /quantify/auth/requirements.txt
RUN pip install --upgrade -r /quantify/auth/requirements.txt

ADD src/auth /quantify/auth
# TODO: add utils dependency

EXPOSE 8080
WORKDIR /quantify
ENV PYTHONPATH /quantify
CMD ["python3.6", "auth/accounts.py"]
