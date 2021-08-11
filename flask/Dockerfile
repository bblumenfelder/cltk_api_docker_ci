FROM ubuntu:20.04
WORKDIR /
COPY macronizer /
ENV TZ=Europe/Berlin
ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y tzdata && apt-get install -y \
    git \
    sudo \
    build-essential \
    libfl-dev \
    unzip 
RUN  useradd admin && echo "admin:admin" | chpasswd && adduser admin sudo
USER admin
RUN sudo unzip RFTagger.zip
RUN sudo chmod -R 777 RFTagger
RUN cd RFTagger/src && make && make install && cd ../.. && sudo ./train-rftagger.sh
COPY requirements.txt import_corpora.py /
ADD . /
RUN pip install -r requirements.txt
RUN python import_corpora.py

CMD ["uwsgi", "app.ini"]