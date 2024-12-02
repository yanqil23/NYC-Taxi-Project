import pandas as pd
import sys
import os

def process_file(input_file_base):
    try:
        # 添加 .csv 后缀来生成输入文件名
        input_file = f"{input_file_base}.csv"

        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            print(f"error: File '{input_file}' not found.")
            return

        # 读取CSV文件
        df = pd.read_csv(input_file)

        # 过滤数据
        filtered_df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 60) &
                         (df['tip_amount'] >= 0) & (df['tip_amount'] < 60)]

        # 生成过滤后的输出文件名
        filtered_output_file = f"{input_file_base}_filtered.csv"

        # 保存过滤后的数据
        filtered_df.to_csv(filtered_output_file, index=False)
        print(f"done: {filtered_output_file}")

        # 计算统计信息
        tip_sum = filtered_df['tip_amount'].sum()
        total_sum = filtered_df['total_amount'].sum()
        row_count = len(filtered_df)

        # 创建统计信息DataFrame
        stats_df = pd.DataFrame({
            'Year_Month': [input_file_base],  # 作为第一列
            'Total_Tip_Amount': [tip_sum],      # 总小费
            'Total_Amount': [total_sum],        # 总金额
            'Row_Count': [row_count]            # 行数
        })

        # 生成统计信息输出文件名
        stats_output_file = f"{input_file_base}_stats.csv"

        # 保存统计信息
        stats_df.to_csv(stats_output_file, index=False)
        print(f"done: {stats_output_file}")

    except pd.errors.EmptyDataError:
        print("error: The input file is empty or invalid.")
    except pd.errors.ParserError as e:
        print(f"error: Parsing CSV failed - {e}")
    except KeyError as e:
        print(f"error: Missing expected column - {e}")
    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python process_file.py <input_file_base>")
    else:
        process_file(sys.argv[1])
