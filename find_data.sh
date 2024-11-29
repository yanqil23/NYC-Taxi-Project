#!/bin/bash

raw_data_urls="raw_data_urls.txt"
wget -q https://github.com/toddwschneider/nyc-taxi-data/raw/master/setup_files/raw_data_urls.txt -O "$raw_data_urls"

if [[ ! -f "$raw_data_urls" ]]; then
    echo "Error downloading raw_data_urls.txt"
    exit 1
fi

filtered_year_months="filtered_year_months.txt"

grep "^https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_" "$raw_data_urls" | \
    while read url; do
        year_month=$(echo "$url" | sed -E 's/.*yellow_tripdata_([0-9]{4}-[0-9]{2}).*/\1/')
        if [[ ! -z "$year_month" ]]; then
            echo "$year_month"  # Output only the year and month
        fi
    done > "$filtered_year_months"

echo "Filtered year-month values have been saved to $filtered_year_months"
