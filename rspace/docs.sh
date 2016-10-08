#!/usr/bin/env bash

dest=${1:-./build_html}

mkdir -p $dest
sphinx-build rspace/docs/ $dest

echo "run \"python -m SimpleHTTPServer\" on $dest"
