FROM ubuntu:20.04
WORKDIR /
COPY macronizer /
ENV TZ=Europe/Berlin
ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y tzdata && apt-get install -y \
    python3-dev \
    python3-pip \
    python-is-python3 \
    python3-psycopg2 \
    git \
    sudo \
    build-essential \
    libfl-dev \
    unzip 
RUN git clone https://github.com/Alatius/morpheus.git
RUN cd morpheus/src && make && make install && cd .. && ./update.sh && ./update.sh && echo "salve" | MORPHLIB=stemlib bin/cruncher -L
RUN useradd admin && echo "admin:admin" | chpasswd && adduser admin sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> \
    /etc/sudoers
RUN sudo unzip RFTagger.zip
RUN sudo chmod -R 777 RFTagger
RUN sudo chmod -R 777 rftagger-ldt.model
RUN cd RFTagger/src && sudo make && sudo make install && cd ../..
USER admin
RUN sudo chmod -R 777 ./train-rftagger.sh && ./train-rftagger.sh
COPY requirements.txt import_corpora.py /
ADD . /
RUN sudo pip install -r requirements.txt
RUN python import_corpora.py

CMD ["uwsgi", "app.ini"]