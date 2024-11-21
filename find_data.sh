#!/bin/bash

raw_data_urls="raw_data_urls.txt"
wget -q https://github.com/toddwschneider/nyc-taxi-data/raw/master/setup_files/raw_data_urls.txt -O "$raw_data_urls"

if [[ ! -f "$raw_data_urls" ]]; then
    echo "Error downloading raw_data_urls.txt"
    exit 1
fi

filtered_urls="filtered_yellow_tripdata_urls.txt"

grep "^https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_" "$raw_data_urls" | \
    while read url; do
        year_month=$(echo "$url" | sed -E 's/.*yellow_tripdata_([0-9]{4}-[0-9]{2}).*/\1/')
        if [[ ! -z "$year_month" ]]; then
            echo "$url,$year_month.csv"
        fi
    done > "$filtered_urls"

echo "Filtered URLs and output file names have been saved to $filtered_urls"
