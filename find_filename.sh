#!/bin/bash

# 设置文件夹路径和输出文件路径
folder_path="./data"  # 替换为目标文件夹路径
output_file="csv_files.txt"  # 输出的文本文件路径

# 获取文件夹中所有.csv文件的文件名（不包括扩展名）
for csv_file in "$folder_path"/*.csv; do
  # 提取文件名并去掉扩展名
  filename=$(basename "$csv_file" .csv)
  echo "$filename" >> "$output_file"
done

echo "文件名已写入 $output_file"
