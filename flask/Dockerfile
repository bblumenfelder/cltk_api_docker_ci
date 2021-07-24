FROM python:3.7-stretch
WORKDIR /
COPY requirements.txt import_corpora.py /
RUN pip install -r requirements.txt
RUN python import_corpora.py
ADD . /
CMD ["uwsgi", "app.ini"]