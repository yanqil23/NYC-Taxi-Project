import pandas as pd
import sys

# Check for correct usage
if len(sys.argv) != 2:
    print("Usage: python process_parquet_to_csv.py <year_month>")
    sys.exit(1)

year_month = sys.argv[1]
output_base = year_month

# Generate the input URL from the year and month
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
input_url = f"{base_url}yellow_tripdata_{year_month}.parquet"

pickup_counts_output = f"{output_base}_pickup_counts.csv"
dropoff_counts_output = f"{output_base}_dropoff_counts.csv"

try:
    # Read the parquet file directly from the generated URL
    print(f"Reading parquet file from URL: {input_url}")
    df = pd.read_parquet(input_url)

    # Calculate pickup and drop-off location counts
    print("Calculating pickup and drop-off location counts...")
    pickup_counts = df['PULocationID'].value_counts()
    dropoff_counts = df['DOLocationID'].value_counts()

    # Write the pickup and drop-off counts to separate CSVs
    print(f"Writing pickup location counts to: {pickup_counts_output}")
    pickup_counts.to_csv(pickup_counts_output, header=["count"])

    print(f"Writing drop-off location counts to: {dropoff_counts_output}")
    dropoff_counts.to_csv(dropoff_counts_output, header=["count"])

    print(f"Successfully processed data for {year_month}")

except Exception as e:
    # Enhanced error reporting
    print(f"Error processing data for {year_month}: {e}")
    sys.exit(1)
