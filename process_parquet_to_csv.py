import pandas as pd
import sys
import re

# Check for correct usage
if len(sys.argv) != 2:
    print("Usage: python process_parquet_to_csv.py <raw_data_urls>")
    sys.exit(1)

raw_data_urls = sys.argv[1]

# Define column selection for 2009 data
columns_2009 = {
    "Trip_Pickup_DateTime": "pickup_datetime",
    "Trip_Dropoff_DateTime": "dropoff_datetime",
    "Passenger_Count": "passenger_count",
    "Trip_Distance": "trip_distance",
    "Tip_Amt": "tip_amount",
    "Total_Amt": "total_amount",
}

# Define default column selection
columns_default = [
    "pickup_datetime",
    "dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount",
]

# Define the date format
date_format = "%Y-%m-%d %H:%M:%S"

def extract_year_month_from_url(url):
    """Extract year and month from the URL."""
    match = re.search(r"yellow_tripdata_(\d{4}-\d{2})", url)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Invalid URL format: {url}")

try:
    with open(raw_data_urls, "r") as file:
        for url in file:
            url = url.strip()

            try:
                # Generate output CSV filename
                year_month = extract_year_month_from_url(url)
                output_csv = f"{year_month}.csv"
                print(f"Processing file from URL: {url}")

                # Read the Parquet file directly from URL
                df = pd.read_parquet(url)

                # Check if file is from 2009
                if "2009" in url:
                    columns_to_select = list(columns_2009.keys())
                    rename_mapping = columns_2009
                    datetime_columns = ["Trip_Pickup_DateTime", "Trip_Dropoff_DateTime"]
                else:
                    columns_to_select = columns_default
                    rename_mapping = None
                    datetime_columns = ["pickup_datetime", "dropoff_datetime"]

                # Select relevant columns
                df_selected = df[columns_to_select]

                # Rename columns for 2009 data to match other years
                if rename_mapping:
                    print("Renaming columns to standard format...")
                    df_selected.rename(columns=rename_mapping, inplace=True)

                # Convert datetime columns
                print("Converting datetime columns...")
                for col in datetime_columns:
                    df_selected[col] = pd.to_datetime(df_selected[col], format=date_format, errors="coerce")

                # Detect missing values and log them
                print("Detecting missing values...")
                missing_values = df_selected.isnull().sum()
                print("Missing values per column:")
                print(missing_values)

                # Optional: Drop rows with missing datetime values
                print("Dropping rows with missing datetime values...")
                df_selected = df_selected.dropna()

                # Write the processed data to CSV
                print(f"Writing to CSV: {output_csv}")
                df_selected.to_csv(output_csv, index=False)
                print(f"Successfully processed {url} to {output_csv}")

            except Exception as e:
                print(f"Error processing file {url}: {e}")

except FileNotFoundError:
    print(f"File {raw_data_urls} not found.")
    sys.exit(1)
