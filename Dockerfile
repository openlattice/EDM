FROM openlattice/base:v0.2

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /controller
ADD controller /controller

ENTRYPOINT ["python", "-u", "/controller/run.py"]
