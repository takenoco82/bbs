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

# test functions
function testing() {
  local size="$1"
  local directory="$2"
  pytest -m $size $directory
}
function medium_test() {
  info "medium test start"
  testing medium $SCRIPT_DIR
}
function large_test() {
  info "large test start"
  testing large $SCRIPT_DIR
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
      uwsgi --ini uwsgi.ini
      ;;
    dev)
      info "develop server start"
      # Quickstart — Flask Documentation (1.1.x) - Externally Visible Server
      #   https://flask.palletsprojects.com/en/1.1.x/quickstart/
      flask run --host 0.0.0.0 --port 5000
      ;;
    test)
      # NOTE 今はまだないのでコメントアウトしておく
      # medium_test
      # large_test
      ;;
    help) usage; exit 0 ;;
    *) exec "$@" ;;
  esac
}

main "$@"
