#!/usr/bin/env Rscript

# 检查输入参数
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: process_parquet_to_csv.R <input_parquet> <output_csv>")
}

# 获取输入和输出文件路径
input_parquet <- args[1]
output_csv <- args[2]

# 加载所需库
if (!require("arrow")) install.packages("arrow", repos = "http://cran.us.r-project.org")
library(arrow)

# 指定需要的列
columns_to_select <- c(
  "tpep_pickup_datetime",
  "tpep_dropoff_datetime",
  "Passenger_count",
  "Trip_distance",
  "Tip_amount",
  "Total_amount"
)

# 读取 Parquet 文件并提取所需列
tryCatch({
  df <- read_parquet(input_parquet, col_select = columns_to_select)
  
  # 写入到 CSV 文件
  write.csv(df, file = output_csv, row.names = FALSE)
  cat(sprintf("Successfully processed %s to %s\n", input_parquet, output_csv))
}, error = function(e) {
  cat(sprintf("Error processing file %s: %s\n", input_parquet, e$message))
})
