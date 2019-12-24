FROM python:3.7.5-alpine

# change timezone
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata

# install develop packages
RUN apk add --no-cache --virtual=develop-deps \
        bash \
        ctags \
        docker \
        git \
        jq \
        less \
        make \
        openssh \
        vim \
        zsh
# install awscli
RUN apk add --no-cache --virtual=awscli-deps groff && \
    pip install --upgrade pip && \
    pip install --no-cache-dir awscli && \
    # install mycli
    apk add --no-cache --virtual=mycli-deps \
        gcc \
        libffi-dev \
        musl-dev \
        openssl-dev && \
    pip install --no-cache-dir mycli && \
    # install docker-compose
    #   https://wiki.alpinelinux.org/wiki/Docker#Docker_Compose
    apk add --no-cache --virtual=docker-compose-deps \
        python-dev \
        libffi-dev \
        openssl-dev \
        gcc \
        libc-dev && \
    pip install --no-cache-dir docker-compose && \
    apk del mycli-deps docker-compose-deps

# install starship
RUN wget https://github.com/starship/starship/releases/download/v0.22.0/starship-x86_64-unknown-linux-musl.tar.gz && \
    tar -xzf starship-x86_64-unknown-linux-musl.tar.gz && \
    mv starship /usr/local/bin/ && \
    rm starship-x86_64-unknown-linux-musl.tar.gz

# install python package manager
ENV POETRY_VERSION=1.0.0
RUN apk add --no-cache curl && \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
    ln -s -f $HOME/.poetry/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.in-project true

# application configure
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV BBS_APP_CONFIG=development

# create the directory to place logfile and uwsgi pid file
RUN mkdir -p \
    /var/log/bbs \
    /var/run/bbs

# listen port
EXPOSE 3031

# install default & develop packages of python to virtualenv
WORKDIR /workspace/backend
# poetry install で必要になるパッケージをインストールする
RUN apk add --no-cache --virtual=uwsgi-deps \
    gcc \
    libc-dev \
    linux-headers

# https://code.visualstudio.com/docs/remote/containers-advanced#_avoiding-extension-reinstalls-on-container-rebuild
RUN mkdir -p $HOME/.vscode-server

# NOTE: 結局マウントするけど、コピーしておかないと起動時にエラーになるのでコピーしておく
COPY ./.devcontainer ./.devcontainer
ENTRYPOINT [ "sh", "./.devcontainer/docker-entrypoint.sh" ]
