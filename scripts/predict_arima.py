import pandas as pd
import numpy as np
import pmdarima as pm
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import argparse
import os

# Function to calculate deviation
def deviation(actual, predicted):
    if(actual > 0):
        return min((abs(actual - predicted) / actual), 1)
    elif(actual == 0 and predicted > 0):
        return 1
    else: return 0

def main(log_dirs, turns):
    devs = []
    vehicle_classes = ['Car', 'Truck', 'Bus', 'LCV', 'Two-Wheeler', 'Three-Wheeler', 'Bicycle']

    for turn in turns:
        train_1 = os.path.join(log_dirs[0], f'{turn}_15s.csv')
        train_2 = os.path.join(log_dirs[1], f'{turn}_15s.csv')
        test_1 = os.path.join(log_dirs[2], f'{turn}_15s.csv')
        test_2 = os.path.join(log_dirs[3], f'{turn}_15s.csv')

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

        # get length of training data
        train_len = len(train_df)
        test_df['seconds'] = test_df['seconds'] + 1800 # Adjust the seconds in the test set to start from the end of the training set

        
        for vehicle in vehicle_classes:
            test_df[vehicle] = test_df[vehicle] + train_df[vehicle].iloc[-1] # Adjust the test set counts to start from the end of the training set

        # Set the seconds as the index
        train_df.set_index('seconds', inplace=True)
        test_df.set_index('seconds', inplace=True)

        # Loop through each vehicle class
        for vehicle in vehicle_classes:
            # Select the column for the current vehicle class
            train_vehicle_counts = train_df[vehicle]
            
            # Fit the ARIMA model on the training data
            model = pm.auto_arima(train_vehicle_counts, start_p = 0, start_q = 0, max_p = 5, max_q = 5, seasonal=True, stepwise=False, suppress_warnings=True, error_action="ignore",random=True,n_fits=50,method="lbfgs",maxiter=200)

            # Forecast on the test set
            n_periods = len(train_df)
            forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)

            # Round the forecasted values to the nearest integer
            forecast = np.round(forecast)

            # Create a DataFrame for the forecast
            forecast_index = range(train_vehicle_counts.index[-1] + 1, train_vehicle_counts.index[-1] + n_periods + 1)
            forecast_df = pd.DataFrame({'seconds': forecast_index, f'{vehicle} Forecast': forecast, 'Lower CI': np.round(conf_int[:, 0]), 'Upper CI': np.round(conf_int[:, 1])})

            devs.append(deviation(test_df[vehicle].iloc[-1] - train_df[vehicle].iloc[-1], forecast_df[f'{vehicle} Forecast'].iloc[-1] - train_df[vehicle].iloc[-1]))

    if devs:
        final_pred_dev = (sum(devs)/(len(turns)*len(vehicle_classes)))*100
        print(f"Final predicted deviation = {final_pred_dev:.3f} %")
    else:
        print("No data processed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run ARIMA model on vehicle count data from log files.")
    parser.add_argument("--log_dirs", nargs=4, required=True, metavar=('TRAIN1_DIR', 'TRAIN2_DIR', 'TEST1_DIR', 'TEST2_DIR'),
                        help="Four log directories for train1, train2, test1, and test2 data.")
    parser.add_argument("--turns", nargs='+', required=True, help="List of turns to process (e.g., BC BE DA).")
    args = parser.parse_args()
    main(args.log_dirs, args.turns)
