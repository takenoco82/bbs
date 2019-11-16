#!/bin/bash

set -eux

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)
readonly PROJECT_DIR=$(cd ${SCRIPT_DIR}; git rev-parse --show-toplevel)
# home directory of the host machine
readonly LOCALHOST_HOME=/localhost_home

# copy ssh config into container works
mkdir -p ~/.ssh
cp -r ${LOCALHOST_HOME}/.ssh/* ~/.ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*

# dotfiles
find ${SCRIPT_DIR}/dotfiles -type f | grep -v sample | while read file; do
  filename=$(basename $file)
  ln -s -f $file ~/${filename}
done

# configure your custom settings
if [[ -e ${SCRIPT_DIR}/user-settings.sh ]]; then
  sh ${SCRIPT_DIR}/user-settings.sh
fi
