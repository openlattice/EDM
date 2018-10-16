FROM debian:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip

RUN mkdir /edm-controller
ADD data /edm-controller
RUN mkdir /data

RUN mkdir /datascience-tools
WORKDIR /datascience-tools
RUN git clone https://github.com/LatticeWorks/datascience-tools.git
WORKDIR /datascience-tools/api-clients
RUN python setup.py install

ENTRYPOINT ["python", "-u", "/edm-controller/run.py"]
