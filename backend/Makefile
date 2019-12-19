include .env

$(eval PROJECT_DIR := $(shell git rev-parse --show-toplevel))
$(eval PROJECT_DIR_NAME := $(shell basename ${PROJECT_DIR}))

DEVCONTAINER_DIR = ${PROJECT_DIR}/backend/.devcontainer

DOCKER_COMPOSE_FILE = ${PROJECT_DIR}/backend/docker-compose.yml
DOCKER_COMPOSE_PRODUCTION_FILE = ${PROJECT_DIR}/backend/docker/local/docker-compose.production.yml

# コマンドの一覧
#   make だけで実行されたときに実行される
list:
	@echo "Target is required. There are the following targets.\n" 1>&2
	@grep -E "^\w+" Makefile | sed "1,/list/d" | sed "s/:.*//"

# コンテナ、ネットワーク、ボリュームの削除
clean:
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		down -v

# ビルド
build:
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${DOCKER_COMPOSE_PRODUCTION_FILE} \
		build

# アプリケーションの停止
stop:
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${DOCKER_COMPOSE_PRODUCTION_FILE} \
		rm --stop --force

# アプリケーションの起動
run: stop build
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${DOCKER_COMPOSE_PRODUCTION_FILE} \
		up -d
	docker-compose ps

# テストの実行
#   make run で起動するアプリケーションとは別のプロセスとして実行される
test:
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${PROJECT_DIR}/backend/docker/local/docker-compose.test.yml \
		-p ${PROJECT_DIR_NAME}_test \
		up --build ap
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${PROJECT_DIR}/backend/docker/local/docker-compose.test.yml \
		-p ${PROJECT_DIR_NAME}_test \
		down -v

# DBマイグレーションの実行
db_migrate: build
	docker run --rm -i -t --network bbs_default \
		${IMAGE_AP_REPOSITORY}:${IMAGE_AP_TAG} \
		flask db upgrade

# DBの初期化
db_init:
	docker run --rm -i -t --network bbs_default \
		mysql:8.0.15 \
		bash -c 'MYSQL_PWD=${MYSQL_PASSWORD} mysql -h db -u ${MYSQL_USER} ${MYSQL_DATABASE} -e \
				"DROP DATABASE IF EXISTS ${MYSQL_DATABASE}; CREATE DATABASE ${MYSQL_DATABASE};"'

# 開発用のイメージをビルド
build_dev:
	docker build \
		-f ${DEVCONTAINER_DIR}/Dockerfile \
		-t ${IMAGE_AP_REPOSITORY}:development .

# コンテナ、イメージ、ネットワーク、ボリュームの削除
clean_all: clean
	docker image ls -q ${IMAGE_AP_REPOSITORY} | xargs docker image rm -f
	# noneなイメージを削除
	docker image ls -q -f "dangling=true" | xargs docker image rm -f
