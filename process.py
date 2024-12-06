import pandas as pd
import sys

def process_parquet_from_url(year_month):
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    input_url = f"{base_url}yellow_tripdata_{year_month}.parquet"

    columns_2011_2024 = {
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
        "passenger_count": "passenger_count",
        "trip_distance": "trip_distance",
        "tip_amount": "tip_amount",
        "total_amount": "total_amount",
        "PULocationID": "PULocationID",
        "DOLocationID": "DOLocationID"
    }

    try:
        print(f"Reading Parquet file from: {input_url}")
        df = pd.read_parquet(input_url, engine='pyarrow')

        columns_to_select = list(columns_2011_2024.keys())
        df_selected = df[columns_to_select]

        print("Renaming columns...")
        df_selected = df_selected.rename(columns=columns_2011_2024)

        print("Converting datetime columns...")
        for col in ["pickup_datetime", "dropoff_datetime"]:
            df_selected.loc[:, col] = pd.to_datetime(df_selected[col], errors='coerce')

        print("Dropping rows with missing values in any column...")
        df_selected = df_selected.dropna()

        print("Filtering data...")
        filtered_df = df_selected[(
            df_selected['trip_distance'] > 0) & (df_selected['trip_distance'] < 60) &
            (df_selected['tip_amount'] >= 0) & (df_selected['tip_amount'] < 60)
        ]

        filtered_output_file = f"{year_month}_filtered.csv"
        filtered_df.to_csv(filtered_output_file, index=False)
        print(f"Filtered file written: {filtered_output_file}")

        print("Calculating pickup location counts...")
        pickup_counts = filtered_df['PULocationID'].value_counts().sort_index()
        pickup_counts.to_csv(f"{year_month}_pickup_counts.csv", header=["count"])

        print("Calculating drop-off location counts and tip stats...")
        dropoff_counts = filtered_df['DOLocationID'].value_counts().sort_index()
        dropoff_tip_totals = filtered_df.groupby('DOLocationID')['tip_amount'].sum().sort_index()
        average_tips = dropoff_tip_totals / dropoff_counts

        dropoff_results = pd.DataFrame({
            'count': dropoff_counts,
            'average_tip': average_tips
        })
        dropoff_results.to_csv(f"{year_month}_dropoff_counts_tip.csv")

        print(f"Successfully processed data for {year_month}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <year_month>")
    else:
        year_month = sys.argv[1]
        process_parquet_from_url(year_month)
