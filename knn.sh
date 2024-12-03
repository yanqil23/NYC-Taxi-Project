#!/bin/bash


if [ $# -ne 1 ]; then
    echo "Usage: $0 <time>"
    echo "Example: $0 2018-01"
    exit 1
fi


TIME=$1



INPUT_DIR="/home/groups/STAT_DSCP/group9/data"
OUTPUT_DIR="/home/groups/STAT_DSCP/group9/jelly"

INPUT_FILE="$INPUT_DIR/${TIME}.csv"


OUTPUT_FILE="$OUTPUT_DIR/r2_score_${TIME}.csv"


if [ -f "$INPUT_FILE" ]; then
    echo "Processing $INPUT_FILE..."


    python3 knn.py process_trip_data "$INPUT_FILE" "$OUTPUT_FILE"

    echo "Output saved to $OUTPUT_FILE."
else
    echo "Input file $INPUT_FILE does not exist. Please check the time and try again."
    exit 1
fi

echo "Processing completed for $TIME."
