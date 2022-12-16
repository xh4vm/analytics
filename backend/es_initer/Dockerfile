FROM python:3.10-slim AS es-initer-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl tini \
    && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=es-initer-builder /opt /opt
COPY --from=es-initer-builder /usr/bin/tini /usr/bin/tini

RUN mkdir /var/log/elasticsearch-initer

WORKDIR /opt/es_initer
ENTRYPOINT [ "tini", "--" ]
CMD [ "python3", "./src/main.py" ]

COPY ./src ./src
RUN pip install --no-index --find-links=/opt/wheels -r ../requirements.txt