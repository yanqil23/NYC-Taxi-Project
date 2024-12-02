#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE=$1

echo "Processing data from $INPUT_FILE..."
python process_file.py "$INPUT_FILE"
if [ $? -ne 0 ]; then
    echo "Failed to process data from $INPUT_FILE"
    exit 1
fi

echo "Successfully processed $INPUT_FILE"
