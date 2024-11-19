import pandas as pd
import sys

# 检查输入参数
if len(sys.argv) != 3:
    print("Usage: python process_parquet_to_csv.py <input_parquet> <output_csv>")
    sys.exit(1)

# 获取输入和输出文件路径
input_parquet = sys.argv[1]
output_csv = sys.argv[2]

# 指定需要的列
columns_to_select = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "Passenger_count",
    "Trip_distance",
    "Tip_amount",
    "Total_amount"
]

try:
    # 读取 Parquet 文件
    df = pd.read_parquet(input_parquet, engine="pyarrow")
    
    # 筛选指定列
    df_selected = df[columns_to_select]
    
    # 保存为 CSV 文件
    df_selected.to_csv(output_csv, index=False)
    
    print(f"Successfully processed {input_parquet} to {output_csv}")

except Exception as e:
    print(f"Error processing file {input_parquet}: {e}")
    sys.exit(1)
