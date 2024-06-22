# * coding utf-8 *
# @author: @github/sounishnath003
# createdAt: 22-04-2024

FROM python:3.11-slim

ARG WORKDIR=/template/app
ENV WORKDIR=${WORKDIR}
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY requirements.txt .
COPY setup.py .
COPY appp ${WORKDIR}/appp

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py install

COPY --from=apache/beam_python3.11_sdk:2.56.0 /opt/apache/beam /opt/apache/beam

ENTRYPOINT ["/opt/apache/beam/boot"]