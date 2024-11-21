#!/bin/bash

# ./process_data.sh <url> <output_csv>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <url> <output_csv>"
    exit 1
fi

URL=$1
OUTPUT_CSV=$2

echo "Downloading data from $URL..."
wget -N $URL
if [ $? -ne 0 ]; then
    echo "Failed to download data from $URL"
    exit 1
fi

FILENAME=$(basename $URL)
if [ ! -f $FILENAME ]; then
    echo "Downloaded file not found: $FILENAME"
    exit 1
fi

echo "Processing data..."
python process_parquet_to_csv.py $FILENAME $OUTPUT_CSV
if [ $? -ne 0 ]; then
    echo "Failed to process data from $FILENAME"
    exit 1
fi

echo "Successfully processed $URL to $OUTPUT_CSV"
