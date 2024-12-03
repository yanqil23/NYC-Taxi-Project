import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor

def process_trip_data(input_file, output_file):

    df = pd.read_csv(input_file)
    df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 60) & (df['tip_amount'] > 0)& (df['tip_amount']< 60)]

    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])

    df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()

    selected_columns = ['trip_duration', 'passenger_count', 'trip_distance', 'tip_amount']
    df = df[selected_columns]


    df = df.dropna()


    X = df[['trip_duration', 'passenger_count', 'trip_distance']]
    y = df['tip_amount']

    X = X.head(1000)
    y = y.head(100)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn_model = KNeighborsRegressor(n_neighbors=20, weights='uniform')  
    knn_model.fit(X_train, y_train)

    y_pred = knn_model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    r2_df = pd.DataFrame({'R2_Score': [r2]})
    r2_df.to_csv(output_file, index=False)
