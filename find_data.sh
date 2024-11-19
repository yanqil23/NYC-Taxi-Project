#!/bin/bash

raw_data_urls="raw_data_urls.txt"
wget -q https://github.com/toddwschneider/nyc-taxi-data/raw/master/setup_files/raw_data_urls.txt -O "$raw_data_urls"

if [[ ! -f "$raw_data_urls" ]]; then
    echo "下载 raw_data_urls.txt 文件失败"
    exit 1
fi

filtered_urls="filtered_yellow_tripdata_urls.txt"

grep "^https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_" "$raw_data_urls" > "$filtered_urls"

