FROM ubuntu:20.04
WORKDIR /
COPY macronizer /
ENV TZ=Europe/Berlin
ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y tzdata && apt-get install -y \
    python3-dev \
    python3-pip \
    python-is-python3 \
    git \
    build-essential \
    libfl-dev \
    unzip \
    python3-psycopg2 
RUN git clone https://github.com/Alatius/morpheus.git
RUN cd morpheus/src && make && make install && cd .. && ./update.sh && ./update.sh && echo "salve" | MORPHLIB=stemlib bin/cruncher -L
RUN unzip RFTagger.zip && cd RFTagger/src && make && make install && cd ../.. && ./train-rftagger.sh
COPY requirements.txt import_corpora.py /
ADD . /
RUN pip install -r requirements.txt
RUN python import_corpora.py

CMD ["uwsgi", "app.ini"]