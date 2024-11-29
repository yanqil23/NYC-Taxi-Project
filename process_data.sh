#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

URL=$1

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
python process_parquet_to_csv.py $FILENAME
if [ $? -ne 0 ]; then
    echo "Failed to process data from $FILENAME"
    exit 1
fi

echo "Successfully processed $URL"

