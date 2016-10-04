#!/usr/bin/env bash

# (c) Juan Diego Godoy Robles - PyConES 2016 Almería
set -e

# CONSTANTS
readonly VERSION="0.1"
readonly SCRIPT=$(basename $0)
readonly LOG=./tmp/${SCRIPT%.*}.bash.log
declare -r -a DBCHOICES=("prod" "test" "dev")

declare -a databases
declare -a mails

source ./validation.sh

source ./lib.sh

source ./logger.sh

function setup_file_logger {
  >$LOG
  fileConfig["filename"]=$LOG
  fileConfig["level"]='DEBUG'
  fileConfig["format"]='[%s] %-8s - %-5s - %s\n'
  fileConfig["datefmt"]='%Y-%m-%dT%H:%M:%S,%3N'
  loggers+=('file')
}


function setup_stream_logger {
  streamConfig["level"]='INFO'
  streamConfig["format"]='%-8s:  %s\n'
  loggers+=('stream')
}


function includes {
  local e
  for e in "${@:2}"; do
    [[ "$e" == "$1" ]] && return 0
  done
  return 1
}


function extended_usage {
  cat <<-EOF
usage: $0 [-h] [-d ${DBCHOICES[@]}] [-m MAILS] [-v] fs [host]

Database space inspector.

positional arguments:
  fs                    Target filesystem.
  host                  Target host.

optional arguments:
  -h                    show this help message and exit
  -d ${DBCHOICES[@]}
                        Target database/s
  -f
  -m MAILS              Notification mails.
  -v                    show program's version number and exit

PyConES 2016 - Almería
EOF
}


function usage {
  echo "usage: $0 [-h] [-d ${DBCHOICES[@]}] [-m MAILS] [-v] fs [host]"
} >&2


function arguments {
  while getopts ":d:m:hv" option; do
    case "${option}" in

      d)  db=${OPTARG}
          if ! includes "${db}" "${DBCHOICES[@]}"; then
            usage
            echo "invalid choice: '${db}' (choose from ${DBCHOICES[@]})" >&2
            exit 2
          fi
          databases+=(${db})
          ;;

      m)  mail ${OPTARG}
          if [ $? -ne 0 ]; then
            usage
            exit 2
          fi
          mails+=(${OPTARG})
          ;;

      v)  echo "$0 v${VERSION}"
          exit 0
          ;;

      h)  extended_usage
          exit 0
          ;;

      *)  usage
          exit 2
          ;;
    esac
  done
}


function gbs_formatter {
  local number=$1

  gawk -v number=$number 'BEGIN{printf "%.2f GBs", (number / 1024 / 1024 / 1024 )}'
} 2>/dev/null


function check_space {
  local fs=$1
  local local_host=$2
  local remote_host=$3

  declare -i free

  if ! avaliable_space $fs; then
    log CRITICAL $LINENO "Can't get local free space in: $fs"
    exit 2
  fi

  log INFO $LINENO "Host: $local_host Avaliable space in $fs: $free $(gbs_formatter $free)"

  if [ $local_host != $remote_host ]; then
    if ! avaliable_space $fs $remote_host; then
      log CRITICAL $LINENO "Can't get free remote space in: $remote_host"
      exit 2
    fi
    log INFO $LINENO "Host: $host Avaliable remote space in $fs: $free $(gbs_formatter $free)"
  fi
}


function main {

  arguments $@
  shift $((OPTIND-1))

  [ $# -eq 0 ] && usage && echo "$SCRIPT: error: too few arguments" >&2 && exit 2
  [ $# -gt 2 ] && shift 2 && usage && echo "$SCRIPT: error: unrecognized arguments: $*" >&2 && exit 2

  [ -z "${databases}" ] && databases+=("test")
  [ -z "${mails}" ] && mails+=("klashxx@gmail.com")

  fs=$(filesystem $1)
  if [ $? -ne 0 ]; then
    usage
    exit 2
  fi

  shift
  if [ $# -eq 1 ]; then
    host=$1
  else
    host=$(hostname 2>/dev/null)
  fi

  setup_file_logger
  setup_stream_logger

  local_host=$(hostname 2>/dev/null)

  log INFO $LINENO  "Parameter validation ok"
  log INFO $LINENO  "OS: $(uname)"
  log INFO $LINENO  "host: ${host}"
  log INFO $LINENO  "local_host: ${local_host}"
  log DEBUG $LINENO "databases: ${databases[*]}"
  log DEBUG $LINENO "fs: ${fs}"
  log DEBUG $LINENO "mails: ${mails[*]}"

  check_space $fs $local_host $host

  exit 0
}


main $@
