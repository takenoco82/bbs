include .env

$(eval PROJECT_DIR := $(shell git rev-parse --show-toplevel))
$(eval PROJECT_DIR_NAME := $(shell basename ${PROJECT_DIR}))

DEVCONTAINER_DIR = ${PROJECT_DIR}/.devcontainer

DOCKER_COMPOSE_FILE = ${PROJECT_DIR}/docker-compose.yml
DOCKER_COMPOSE_PRODUCTION_FILE = ${PROJECT_DIR}/docker/local/docker-compose.production.yml

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
		-f ${PROJECT_DIR}/docker/local/docker-compose.test.yml \
		-p ${PROJECT_DIR_NAME}_test \
		up --build ap
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${PROJECT_DIR}/docker/local/docker-compose.test.yml \
		-p ${PROJECT_DIR_NAME}_test \
		down -v

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
