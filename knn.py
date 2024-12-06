import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

def process_trip_data(year_month):
    try:
        print(f"Reading data from: {year_month}")
        df = pd.read_csv(f"{year_month}_filtered.csv")
        df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 60) & (df['tip_amount'] > 0)& (df['tip_amount']< 60)]
        print("Converting datetime columns...")
        df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
        df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

        print("Calculating trip duration...")
        df['trip_duration'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds()
        df = df.dropna()
        print("Preparing data for training...")
        X = df[['trip_duration', 'passenger_count', 'trip_distance']]
        y = df['tip_amount']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a KNN model
        print("Training KNN model...")
        knn_model = KNeighborsRegressor(n_neighbors=20, weights='uniform')
        knn_model.fit(X_train, y_train)

        # Make predictions
        print("Predicting test set...")
        y_pred = knn_model.predict(X_test)

        # Calculate R2 score
        r2 = r2_score(y_test, y_pred)
        print(f"R2 Score: {r2}")

        # Save R2 score to CSV
        output_file = f"{year_month}_r2_score.csv"
        print(f"Saving R2 score to: {output_file}")
        r2_df = pd.DataFrame({'R2_Score': [r2]})
        r2_df.to_csv(output_file, index=False)

    except Exception as e:
        print(f"Error processing trip data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <year_month>")
    else:
        input_csv = sys.argv[1]
        process_trip_data(input_csv)
