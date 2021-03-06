#!/bin/bash

set -eux

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)
readonly PROJECT_DIR=$(cd ${SCRIPT_DIR}/..; pwd)

# install default & develop packages of python to virtualenv
(cd ${PROJECT_DIR}; poetry install)

exec "$@"
