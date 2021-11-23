# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /flask/user
ENV FLASK_APP=user
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install --upgrade -v pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /flask
EXPOSE 5001
CMD ["flask", "run","-p","5001"]