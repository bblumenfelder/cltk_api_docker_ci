FROM ubuntu:20.04
ENV LANG C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
WORKDIR /
COPY macronizer /
ENV TZ=Europe/Berlin
ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y tzdata && apt-get install -y \
    python3-dev \
    python3-pip \
    python-is-python3 \
    locales \
    git \
    sudo \
    build-essential \
    libfl-dev \
    unzip \
    python3-psycopg2 
RUN locale-gen en_US.UTF-8
RUN cat app.py
RUN git clone https://github.com/Alatius/morpheus.git
RUN cd morpheus/src && make && make install && cd .. && ./update.sh && ./update.sh && echo "salve" | MORPHLIB=stemlib bin/cruncher -L
# Add none root user
RUN sudo unzip RFTagger.zip && sudo chmod -R 777 RFTagger && cd RFTagger/src && make && make install && cd ../.. && sudo chmod -R 777 ./train-rftagger.sh && ./train-rftagger.sh
COPY requirements.txt import_corpora.py /
ADD . /
RUN pip install -r requirements.txt
RUN python import_corpora.py
CMD ["uwsgi", "app.ini"]