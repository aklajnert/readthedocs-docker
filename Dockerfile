FROM aklajnert/snakepit:2.1-bullseye-slim

RUN set -ex && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
		build-essential \
		texlive-latex-recommended \
        texlive-fonts-recommended \
        texlive-latex-extra \
        latexmk \
        texlive-luatex \
        texlive-xetex \
        libssl-dev \
        libghc-zlib-dev \
        libcurl4-gnutls-dev \
        libexpat1-dev \
        gettext && \
    # rtd requires git > 2.17, apt-get is capable to install 2.11, so it needs to be built from sources
    wget https://github.com/git/git/archive/v2.21.0.tar.gz -O git.tar.gz && \
    tar -zxf git.tar.gz && \
    cd git-* && \
    make prefix=/usr/local NO_TCLTK=YesPlease install && \
    git --version && \
    cd .. && \
    rm -rf git*

RUN git clone --branch 4.1.2 --recurse-submodules https://github.com/rtfd/readthedocs.org.git

WORKDIR readthedocs.org
SHELL ["/bin/bash", "-c"]

RUN set -ex && \
    python2.7 -m pip install virtualenv && \
    python3.5 -m pip install virtualenv && \
    python3.6 -m pip install virtualenv && \
    python3.7 -m pip install virtualenv && \
    python3.8 -m pip install virtualenv && \
    python3.6 -m venv /venv && \
        source /venv/bin/activate && \
        python3.6 -m pip install -r requirements/docker.txt gunicorn

COPY docker-settings.py readthedocs/settings/docker.py

ENV DJANGO_SETTINGS_MODULE=readthedocs.settings.docker

COPY entrypoint.py ./

EXPOSE 8000 8088

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

ENTRYPOINT ["/venv/bin/python", "-u", "entrypoint.py"]
