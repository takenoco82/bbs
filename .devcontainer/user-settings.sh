#!/bin/bash

set -eux

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)
readonly PROJECT_DIR=$(cd ${SCRIPT_DIR}; git rev-parse --show-toplevel)
# home directory of the host machine
readonly LOCALHOST_HOME=/localhost_home
