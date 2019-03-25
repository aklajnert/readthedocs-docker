FROM python:3.6.8-alpine3.9

RUN apk update && apk add git g++ gcc libxslt-dev uwsgi uwsgi-python3

RUN git clone --recurse-submodules https://github.com/rtfd/readthedocs.org.git

WORKDIR readthedocs.org
RUN pip install -r requirements.txt

COPY docker-settings.py readthedocs/settings/docker.py

ENV DJANGO_SETTINGS_MODULE=readthedocs.settings.docker

COPY uwsgi.ini /etc/uwsgi.ini
COPY entrypoint.py ./

EXPOSE 8000
ENTRYPOINT ["python", "entrypoint.py"]
