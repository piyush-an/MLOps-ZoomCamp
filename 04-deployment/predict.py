import argparse
import os
import pickle
import pandas as pd

with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)
categorical = ['PUlocationID', 'DOlocationID']


def read_data(year:str, month: str):
    df = pd.read_parquet(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year}-{month}.parquet')
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


def main(year:str, month: str):
    df = read_data(year, month)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    print(f"Mean predict value for the year {year} and month {month} is {y_pred.mean():.2f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        default="2021",
        type=str,
        help="year for which prediction to be done, like 2021"
    )
    parser.add_argument(
        "--month",
        default="01",
        type=str,
        help="month two digit, like jan - 01"
    )
    
    args = parser.parse_args()

    if (len(args.year) != 4) or (len(args.month) != 2):
        print("Invalid argument, Example --year=2021 --month=01")
        exit(101)
    
    main(args.year, args.month)
