FROM python:3.7.5-alpine AS base

# change timezone
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata

WORKDIR /bbs

# install python package manager
RUN apk add --no-cache curl && \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
    ln -s -f $HOME/.poetry/bin/poetry /usr/local/bin/poetry

# install default packages of python to system
COPY ./poetry.lock ./pyproject.toml ./
RUN apk add --no-cache --virtual=uwsgi-deps \
    gcc \
    libc-dev \
    linux-headers && \
    poetry config settings.virtualenvs.create false && \
    poetry install --no-dev && \
    apk del uwsgi-deps

# application configure
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# create the directory to place logfile and uwsgi pid file
RUN mkdir -p \
    /var/log/bbs \
    /var/run/bbs


FROM base as test
# application configure
ENV BBS_APP_CONFIG=test

# install develop packages of python to system
RUN poetry install

# copy production, migrations and test code
COPY ./src/docker-entrypoint.sh ./src/run.py ./setup.cfg ./
COPY ./src/.settings ./.settings
COPY ./src/app ./app
COPY ./src/migrations ./migrations
COPY ./src/tests ./tests

# lint
RUN [ "flake8" ]
# small test
RUN [ "pytest", "-m", "small", "tests" ]
# run test
ENTRYPOINT [ "sh", "./docker-entrypoint.sh"]
CMD [ "test" ]


FROM base as production
# application configure
ENV BBS_APP_CONFIG=production

# copy production and migrations code
COPY ./src/docker-entrypoint.sh ./src/run.py ./setup.cfg ./
COPY ./src/.settings ./.settings
COPY ./src/app ./app
COPY ./src/migrations ./migrations

# listen port
EXPOSE 3031

# run application
ENTRYPOINT [ "sh", "./docker-entrypoint.sh"]
CMD [ "run" ]
