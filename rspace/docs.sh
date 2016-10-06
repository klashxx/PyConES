#!/usr/bin/env bash

dest=${1:-/tmp/rspace}

mkdir -p $dest
sphinx-build rspace/docs/ $dest

echo "run \"python -m SimpleHTTPServer\" on $dest"
