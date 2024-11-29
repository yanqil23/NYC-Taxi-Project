#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <year-month>"
    exit 1
fi

YEAR_MONTH=$1
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_${YEAR_MONTH}.parquet"

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

