"""
Main function to simulate missing data in heart rate column in COVID-19 wearables datasets, avaiable at: 
https://storage.googleapis.com/gbsc-gcp-project-ipop_public/COVID-19/COVID-19-Wearables.zip).

Command-line Arguments:
    -m: Missing values mechanism (choices: MCAR, MAR, MNAR)
    -p: Percentage of missing values (integer)
    -n: Number of subfolders to process (integer)

Outputs:
    - CSV files with simulated missing values saved in a structured directory format.
    - Each file is named according to the original file name, mechanism, percentage, and dataset index.
"""

import os
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm

from mdatagen.univariate.uMCAR import uMCAR
from mdatagen.univariate.uMAR import uMAR
from mdatagen.univariate.uMNAR import uMNAR

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Missing data simulator for datasets.")
    parser.add_argument(
        "-m", 
        type=str, 
        required=True, 
        choices=["MCAR", "MAR", "MNAR"], 
        help="Name of the missing data mechanism (choose from: MCAR, MAR, MNAR)."
    )
    parser.add_argument("-p", type=int, required=True, help="Percentage of missing values (e.g., 25, 50, ...).")
    parser.add_argument("-n", type=int, required=True, help="Number of datasets to be generated for each file.")
    args = parser.parse_args()

    mechanism = args.m
    mr = args.p
    num_datasets = args.n

    folder_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'Data', 'COVID-19-Wearables'
    )
    files = [file for file in os.listdir(folder_path) if file.endswith('_hr.csv')]

    for file_name in tqdm(files, desc=f"Processing files for {mr}%", unit="file"):
        file_path = os.path.join(folder_path, file_name)
        try:
            data = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading file {file_name}: {e}")
            continue

        for idx in tqdm(
            range(1, num_datasets + 1),
            desc=f"Generating datasets for {file_name}",
            unit="dataset",
            leave=False
        ):
            match mechanism:
                case "MCAR":
                    X = data[["datetime", "heartrate"]]
                    X.set_index("datetime", inplace=True)
                    generator = uMCAR(X=X, y=data.heartrate.to_numpy(), missing_rate=mr, x_miss="heartrate") 
                    generate_data = generator.random()
                case "MAR":
                    X = data[["datetime", "heartrate"]]
                    X["time"] = pd.to_datetime(X["datetime"]).dt.time
                    generator = uMAR(X=X, y=data.heartrate.to_numpy(), missing_rate=mr, x_miss='heartrate', x_obs='time')
                    generate_data = generator.lowest()
                case "MNAR":
                    X = data[["datetime", "heartrate"]]
                    generator = uMNAR(X=X, y=data.heartrate.to_numpy(), threshold=0, missing_rate=mr, x_miss='heartrate')
                    generate_data = generator.run()
                case _:
                    print(f"Invalid mechanism {mechanism}.")
                    continue

            base_folder = os.path.join(
                os.path.dirname(__file__), '..', '..', 'Data', 'COVID-19-Wearables-Missing'
            )
            mechanism_folder = os.path.join(base_folder, mechanism)
            percentage_folder = os.path.join(mechanism_folder, f'{mr}')
            idx_folder = os.path.join(percentage_folder, f'{idx}')
            os.makedirs(idx_folder, exist_ok=True)

            save_path = os.path.join(
                idx_folder,
                file_name.replace('.csv', f'_{mechanism}_{mr}_{idx}.csv')
            )

            generate_data.reset_index().merge(
                data[["datetime", "user"]], on="datetime"
            )[["user", "datetime", "heartrate", "target"]].to_csv(save_path, index=False)


