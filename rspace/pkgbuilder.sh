#!/usr/bin/env bash

python ./setup.py sdist
code=$?
echo "===================="
if [ $code -ne 0 ];then
   echo "Error build: ${code}"
   echo "===================="
   exit $code
fi
echo "Build ok!"
echo "===================="

