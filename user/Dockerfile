# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /flask/user
ENV FLASK_APP=user
ENV FLASK_RUN_HOST=0.0.0.0


RUN apt-get update
RUN apt-get upgrade
RUN apt-get install libmariadb-dev -y
RUN apt-get install gnutls-bin -y
RUN apt-get install openssl -y
RUN apt-get install libssl-dev -y
RUN apt-get install build-essential -y
RUN apt-get install python3-dev -y 
RUN apt-get install mysql-common -y
RUN apt-get install default-libmysqlclient-dev -y
RUN apt install libpq-dev -y

COPY requirements.txt requirements.txt
RUN pip install --upgrade -v pip
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /flask
EXPOSE 5001
CMD ["flask", "run","-p","5001"]