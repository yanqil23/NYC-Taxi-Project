#!/bin/bash

# Check for correct usage
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <year_month>"
    exit 1
fi

YEAR_MONTH=$1

# Run the Python script with the given year_month parameter
echo "Processing data for: $YEAR_MONTH"

python GBRT.py "$YEAR_MONTH"

# Check if the Python script executed successfully
if [ $? -eq 0 ]; then
    echo "GBRT for $YEAR_MONTH completed successfully."
else
    echo "GBRT for $YEAR_MONTH failed."
    exit 1
fi
