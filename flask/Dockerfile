FROM python:3.9-alpine

WORKDIR /

ADD . /

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]