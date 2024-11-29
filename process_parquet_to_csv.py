import pandas as pd
import sys

# Check for correct usage
if len(sys.argv) != 3:
    print("Usage: python process_parquet_to_csv.py <input_parquet> <output>")
    sys.exit(1)

input_parquet = sys.argv[1]
output = sys.argv[2]
output_csv = f"{output}.csv"


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

# Check if file is from 2009
if "2009" in input_parquet:
    columns_to_select = list(columns_2009.keys())
    rename_mapping = columns_2009
else:
    columns_to_select = columns_default
    rename_mapping = None

try:
    # Read the parquet file
    print(f"Reading parquet file: {input_parquet}")
    df = pd.read_parquet(input_parquet)

    # Select relevant columns
    df_selected = df[columns_to_select]

    # Rename columns for 2009 data to match other years
    if rename_mapping:
        print("Renaming columns to standard format...")
        df_selected.rename(columns=rename_mapping, inplace=True)

    # Convert datetime columns
    print("Converting datetime columns...")
    datetime_columns = ["pickup_datetime", "dropoff_datetime"]
    for col in datetime_columns:
        df_selected[col] = pd.to_datetime(df_selected[col], format=date_format, errors="coerce")

    # Detect missing values and log them
    print("Detecting missing values...")
    missing_values = df_selected.isnull().sum()
    print("Missing values per column:")
    print(missing_values)

    # Optional: Drop rows with missing datetime values (if necessary for your use case)
    print("Dropping rows with missing datetime values...")
    df_selected = df_selected.dropna()

    # Write the processed data to CSV
    print(f"Writing to CSV: {output_csv}")
    df_selected.to_csv(output_csv, index=False)
    print(f"Successfully processed {input_parquet} to {output_csv}")

except Exception as e:
    # Enhanced error reporting
    print(f"Error processing file {input_parquet}: {e}")
    sys.exit(1)
