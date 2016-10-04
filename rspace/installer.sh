#!/usr/bin/env bash

cmd="./setup.py install"
echo "Installing ..."
echo "cmd: ${cmd}"
python ${cmd}
code=$?
echo "================"
echo "install code:${code}"
echo "================"
if [[ $code -ne 0 ]]; then
  exit $code
fi

exit 0
