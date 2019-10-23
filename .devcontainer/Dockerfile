FROM python:3.7.5-alpine

# change timezone
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata

# install develop packages
RUN apk add --no-cache --virtual=develop-deps \
        bash \
        docker \
        git \
        jq \
        less \
        make \
        openssh \
        vim \
        zsh && \
    # install mycli
    apk add --no-cache --virtual=mycli-deps \
        gcc \
        libffi-dev \
        musl-dev \
        openssl-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir mycli && \
    apk del mycli-deps && \
    # install docker-compose
    #   https://wiki.alpinelinux.org/wiki/Docker#Docker_Compose
    apk add --no-cache --virtual=docker-compose-deps \
        python-dev \
        libffi-dev \
        openssl-dev \
        gcc \
        libc-dev && \
    pip install --no-cache-dir docker-compose && \
    apk del docker-compose-deps

# install starship
RUN wget https://github.com/starship/starship/releases/download/v0.22.0/starship-x86_64-unknown-linux-musl.tar.gz && \
    tar -xzf starship-x86_64-unknown-linux-musl.tar.gz && \
    mv starship /usr/local/bin/ && \
    rm starship-x86_64-unknown-linux-musl.tar.gz

# install python package manager
RUN apk add --no-cache curl && \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
    ln -s -f $HOME/.poetry/bin/poetry /usr/local/bin/poetry

# application configure
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# listen port
EXPOSE 5000

# install default & develop packages of python to virtualenv
WORKDIR /workspace
# NOTE: 結局マウントするけど、コピーしておかないと起動時にエラーになるのでコピーしておく
COPY ./.devcontainer ./.devcontainer
ENTRYPOINT [ "sh", "./.devcontainer/docker-entrypoint.sh" ]
