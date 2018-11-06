FROM openlattice/base:v0.1-rc2

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# install openapi straight from openapi-specs
RUN git clone -b feature/openapispecs https://github.com/openlattice/api.git
RUN cd api && \
  ./gradlew generatePythonClient && \
  cd build/openapi/python && \
  python setup.py install

ENTRYPOINT ["python", "-u", "/controller/test_api.py"]
