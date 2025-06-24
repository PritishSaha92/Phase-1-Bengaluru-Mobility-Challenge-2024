import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import argparse
import os

def deviation(actual, predicted):
    if actual > 0:
        return min((abs(actual - predicted) / actual), 1)
    elif actual == 0 and predicted > 0:
        return 1
    else:
        return 0

def main(log_dirs, turns):
    devs = []
    vehicle_classes = ['Car', 'Truck', 'Bus', 'LCV', 'Two-Wheeler', 'Three-Wheeler', 'Bicycle']

    for turn in turns:
        train_1 = os.path.join(log_dirs[0], f'{turn}_60s.csv')
        train_2 = os.path.join(log_dirs[1], f'{turn}_60s.csv')
        test_1 = os.path.join(log_dirs[2], f'{turn}_60s.csv')
        test_2 = os.path.join(log_dirs[3], f'{turn}_60s.csv')

        try:
            train_df_1 = pd.read_csv(train_1, dtype=int)
            train_df_2 = pd.read_csv(train_2, dtype=int)
            test_df_1 = pd.read_csv(test_1, dtype=int)
            test_df_2 = pd.read_csv(test_2, dtype=int)
        except FileNotFoundError as e:
            print(f"Error reading file: {e}. Skipping turn {turn}.")
            continue

        train_df_2 = train_df_2 + train_df_1.iloc[-1]
        test_df_2 = test_df_2 + test_df_1.iloc[-1]

        train_df = pd.concat([train_df_1, train_df_2], ignore_index=True)
        test_df = pd.concat([test_df_1, test_df_2], ignore_index=True)

        # Get length of training data
        train_len = len(train_df)

        # Adjust the seconds in the test set to start from the end of the training set
        test_df['seconds'] = test_df['seconds'] + 900

        # Adjust the test set counts to start from the end of the training set
        for vehicle in vehicle_classes:
            test_df[vehicle] = test_df[vehicle] + train_df[vehicle].iloc[-1]

        # Convert 'seconds' to datetime format
        train_df['ds'] = pd.to_datetime(train_df['seconds'], unit='s')

        # Prepare the data for Prophet
        for vehicle in vehicle_classes:
            df = train_df[['ds', vehicle]]
            df = df.rename(columns={vehicle: 'y'})

            # Initialize and fit the model
            model = Prophet()
            model.fit(df)

            # Make a future dataframe for predictions
            future = model.make_future_dataframe(periods=train_len, freq='S')
            forecast = model.predict(future)

            # Round the prediction values to integers
            forecast['yhat'] = forecast['yhat'].round().astype(int)

            # Get the actual value from the test set (final value)
            actual_value = test_df[vehicle].iloc[-1]

            # Get the predicted value from the forecast (final value)
            predicted_value = forecast['yhat'].iloc[-1]

            # Print the results
            print(f"Turn: {turn}, Vehicle: {vehicle}")
            print(f"Actual: {actual_value}, Predicted: {predicted_value}")
            print("-" * 40)
            devs.append(deviation(actual_value - train_df[vehicle].iloc[-1], predicted_value - train_df[vehicle].iloc[-1]))

    if devs:
        final_pred_dev = (sum(devs)/(len(turns)*len(vehicle_classes)))*100
        print(f"Final Prediction Deviation: {final_pred_dev:.2f}%")
    else:
        print("No data processed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Prophet model on vehicle count data from log files.")
    parser.add_argument("--log_dirs", nargs=4, required=True, metavar=('TRAIN1_DIR', 'TRAIN2_DIR', 'TEST1_DIR', 'TEST2_DIR'),
                        help="Four log directories for train1, train2, test1, and test2 data.")
    parser.add_argument("--turns", nargs='+', required=True, help="List of turns to process (e.g., BC BE DA).")
    args = parser.parse_args()
    main(args.log_dirs, args.turns)
