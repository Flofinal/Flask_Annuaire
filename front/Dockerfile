# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /flask/front
ENV FLASK_APP=front
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install --upgrade -v pip
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install build-essential -y
RUN apt-get install python3-dev -y 
RUN apt-get install mysql-common -y
RUN apt-get install default-libmysqlclient-dev -y
RUN apt install libpq-dev -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /flask
EXPOSE 5000
CMD ["flask", "run","-p","5000"]