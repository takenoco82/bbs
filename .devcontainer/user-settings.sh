#!/bin/bash

set -eux

# home directory of the host machine
LOCALHOST_HOME=/localhost_home

# copy git config into container works
cp -f ${LOCALHOST_HOME}/git/dotfiles/.gitconfig.linux ~/.gitconfig
# ln -s -f ${LOCALHOST_HOME}/git/dotfiles/.gitconfig.linux ~/.gitconfig
