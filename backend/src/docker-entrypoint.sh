#!/bin/sh

set -eu

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)


#
# 関数定義
#

function usage() {
  cat <<EOS >&2
Usage: sh $(pwd)/$(basename "$0") <command>

  DESCRIPTION
    {DESCRIPTION}

  command
    run     Start application
    dev     Start develop server
    test    Run test
    help    Show this help

EOS
}

# logging functions
function logging() {
  local type="$1"; shift
  printf '%s [%s] [Entrypoint]: %s\n' "$(date -Iseconds)" "$type" "$*"
}
function info() {
  logging INFO "$@"
}
function warn() {
  logging WARN "$@" >&2
}
function error() {
  logging ERROR "$@" >&2
  exit 1
}

#
# メイン処理
#
function main() {
  info "Entrypoint script started."

  if [ $# -eq 0 ]; then
    error "command required"
  fi

  case $1 in
    run)
      info "application start"
      uwsgi --ini ${SCRIPT_DIR}/.settings/uwsgi.ini
      ;;
    migrate)
      info "DB migration start"
      flask db current
      flask db upgrade
      flask db history
      ;;
    dev)
      info "develop server start"
      # Quickstart — Flask Documentation (1.1.x) - Externally Visible Server
      #   https://flask.palletsprojects.com/en/1.1.x/quickstart/
      flask run --host 0.0.0.0 --port 5000
      ;;
    lint)
      info "lint start"
      flake8
      ;;
    test)
      info "small test start"
      pytest -m small tests
      ;;
    help) usage; exit 0 ;;
    *) exec "$@" ;;
  esac
}

main "$@"
