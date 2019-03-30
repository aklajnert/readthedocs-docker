FROM aklajnert/snakepit:1.0-alpine-3.9

RUN set -ex && \
    apk update && \
    apk add \
        git \
        g++ \
        gcc \
        libxslt-dev \
        uwsgi \
        uwsgi-python3 \
        postgresql-dev \
        jpeg-dev \
        zlib-dev \
        libmemcached-dev

RUN git clone --recurse-submodules https://github.com/rtfd/readthedocs.org.git

WORKDIR readthedocs.org
RUN set -ex && \
    python2.7 -m pip install virtualenv && \
    python3.5 -m pip install virtualenv && \
    python3.6 -m pip install virtualenv && \
    python3.7 -m pip install virtualenv && \
    python3.6 -m venv /venv && source /venv/bin/activate && pip install -r requirements.txt psycopg2-binary

COPY docker-settings.py readthedocs/settings/docker.py

ENV DJANGO_SETTINGS_MODULE=readthedocs.settings.docker

COPY uwsgi.ini /etc/uwsgi.ini
COPY entrypoint.py ./

EXPOSE 8000

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

ENTRYPOINT ["/venv/bin/python", "-u", "entrypoint.py"]
