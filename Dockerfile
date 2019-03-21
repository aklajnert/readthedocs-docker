FROM python:3.6.8-alpine3.9

RUN apk update && apk add git g++ gcc libxslt-dev

RUN git clone --recurse-submodules https://github.com/rtfd/readthedocs.org.git

WORKDIR readthedocs.org
RUN pip install -r requirements.txt

COPY entrypoint.py /readthedocs.org/entrypoint.py
ENTRYPOINT python3.6 entrypoint.py
