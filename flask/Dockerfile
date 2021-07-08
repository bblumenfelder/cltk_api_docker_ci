FROM python:3.7-stretch

WORKDIR /

ADD . /

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]