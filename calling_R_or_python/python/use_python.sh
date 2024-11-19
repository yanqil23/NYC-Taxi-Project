#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <n_CPU>" 1>&2 # write to stderr
    exit 0
fi
n_CPU=$1

python use_python.py $n_CPU
