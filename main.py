import argparse
import os
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException, Response, status, Query, Request
from fastapi.responses import HTMLResponse

with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)
categorical = ['PUlocationID', 'DOlocationID']

description = """
API helps to provide ML model as a service. 

## Users
You will be able to:
* **Predict Taxi Ride Duration**
"""

tags_metadata = [
    {
        "name": "time",
        "description": "Predicts the mean duration of ride time between two locations",
    },
]

app = FastAPI(  title="NYC Ride Time Predict",
                description=description,)

@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def read_items():
    return """
<html>
   <head>
      <title>Welcome to NYC Ride Prediction</title>
      <style>
         h1 {text-align: center;}
         p {text-align: center;}
         div {text-align: center;}
         #footer {
         position:absolute;
         bottom:0;
         width:100%;
         height:60px;
         }
      </style>
   </head>
   <body>
      <h1 style="text-decoration: underline;">NYC Taxi Ride API</h1>
      <p>This project is a part of MLOps ZoomCamp <a href="https://github.com/DataTalksClub/mlops-zoomcamp" target="_blank">GitHub</a> </p>
      <p style="text-align:center;"><img src="https://github.com/DataTalksClub/mlops-zoomcamp/raw/main/images/banner.png" width="400" height="200"></p>
      
      <p>Explore the API by visitng `/docs` endpoint </p>
   </body>
   <div id="footer">
   <p> Built with <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>
      <p>© 2022 <a href="https://piyushanand.carrd.co/" target="_blank">Piyush Anand</a> </p>
   </div>
   </div>
</html>
    """

def read_data(year:str, month: str):
    df = pd.read_parquet(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year}-{month}.parquet')
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

@app.post("/predict", tags=["time"], status_code=status.HTTP_200_OK)
def predict(year:str, month: str):
    if (len(year) != 4) or (len(month) != 2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid argument, Example year=2021 month=01" )
    df = read_data(year, month)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    return (f"Mean predict value for the year {year} and month {month} is {y_pred.mean():.2f}")

