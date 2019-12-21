include .env

$(eval PROJECT_DIR := $(shell git rev-parse --show-toplevel))

WORKSPACE_DIR = ${PROJECT_DIR}/backend
DEVCONTAINER_DIR = ${WORKSPACE_DIR}/.devcontainer

DOCKER_COMPOSE_FILE = ${WORKSPACE_DIR}/docker-compose.yml
DOCKER_COMPOSE_PRODUCTION_FILE = ${WORKSPACE_DIR}/docker/local/docker-compose.production.yml

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
		-f ${WORKSPACE_DIR}/docker/local/docker-compose.test.yml \
		-p ${IMAGE_AP_REPOSITORY}_test \
		build ap
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${WORKSPACE_DIR}/docker/local/docker-compose.test.yml \
		-p ${IMAGE_AP_REPOSITORY}_test \
		run ap lint
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${WORKSPACE_DIR}/docker/local/docker-compose.test.yml \
		-p ${IMAGE_AP_REPOSITORY}_test \
		run ap test
	docker-compose \
		-f ${DOCKER_COMPOSE_FILE} \
		-f ${WORKSPACE_DIR}/docker/local/docker-compose.test.yml \
		-p ${IMAGE_AP_REPOSITORY}_test \
		down -v

# DBマイグレーションの実行 (開発用)
db_migrate:
	source ./.venv/bin/activate \
		&& cd src \
		&& sh ./docker-entrypoint.sh migrate

# DBの初期化 (開発用)
db_init:
	mycli -d local -e "DROP DATABASE IF EXISTS ${MYSQL_DATABASE}; CREATE DATABASE ${MYSQL_DATABASE};"'

# アプリケーションの起動 (開発用)
dev:
	source ./.venv/bin/activate \
		&& cd src \
		&& sh ./docker-entrypoint.sh dev

# コンテナ、イメージ、ネットワーク、ボリュームの削除
clean_all: clean
	docker image ls -q ${IMAGE_AP_REPOSITORY} | xargs docker image rm -f
	# noneなイメージを削除
	docker image ls -q -f "dangling=true" | xargs docker image rm -f
