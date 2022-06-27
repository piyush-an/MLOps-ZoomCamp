import os
import time
import pickle
import pandas as pd
from google.cloud import storage
from fastapi import FastAPI, HTTPException, Response, status, Query, Request
from fastapi.responses import HTMLResponse

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/key/key.json"

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
      <link rel="icon" type="image/x-icon" href="https://cdn-icons-png.flaticon.com/512/171/171241.png">
      <style>
         h1 {text-align: center;}
         p {text-align: center;}
         div {text-align: center;}
         h3 {text-align: center;}
         #footer {
         position:absolute;
         bottom:0;
         width:100%;
         height:150px;
         }
      </style>
   </head>
   <body>
      <h1 style="text-decoration: underline;">NYC Taxi Ride API</h1>
      <p>This project is a part of <a href="https://github.com/DataTalksClub/mlops-zoomcamp" target="_blank">MLOps ZoomCamp</a> to productionizing a ML services <br> A model to predict the ride duration between two location using <a href="https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page" target="_blank">For-Hire Vehicle Trip Records</a> dataset </p>
      <p style="text-align:center;"> 
         <img src="https://github.com/DataTalksClub/mlops-zoomcamp/raw/main/images/banner.png" width="400" height="200">
         <img src="https://www1.nyc.gov/assets/tlc/images/content/header/NYC-TLC-Pride-Logo.png" width="300" height="200">
      </p>
      <p>Explore the API by visitng `/docs` endpoint <button text-align: center onclick="window.open('https://nyc-taxi.anandpiyush.com/docs','_blank');" type="button"> Try API</button> </p>
      <h3 style="text-decoration: underline;">API Features</h3>
      <p>
         • Predicts the ride duration <br>
         • Exports the predicitions as parquet on GCP Bucket
      </p>
   </body>
   <div id="footer">
      <p> Built with <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>
      <p> Issues & Suggestion <a href="https://github.com/piyush-an/MLOps-ZoomCamp" target="_blank">GitHub</a>
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

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    return f"https://storage.googleapis.com/nyc-taxi-processed/{destination_blob_name}"

def export_parquet(year, month, df, y_pred):
    ts = time.strftime("%Y%m%d-%H%M%S")
    df['ride_id'] = f'{year}/{month}_' + df.index.astype('str')
    df['predictions'] = y_pred
    df_result = df[['ride_id','predictions']].copy()
    file_name = f"/app/predicted_{year}-{month}_{ts}.parquet"
    # file_name = f"/home/mlops_zoomcamp/Notebooks/week04/web_app/predicted_{year}-{month}_{ts}.parquet"
    df_result.to_parquet(file_name,
        engine='pyarrow',
        compression=None,
        index=False)
    return upload_blob("nyc-taxi-processed", file_name, file_name.split('/')[-1])
    

@app.post("/predict", tags=["time"], status_code=status.HTTP_200_OK)
def predict(year:str, month: str):
    if (len(year) != 4) or (len(month) != 2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid argument, Example year=2021 month=01" )
    df = read_data(year, month)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    file_url = export_parquet(year, month, df, y_pred)
    return (f"Mean predict value for the year {year} and month {month} is {y_pred.mean():.2f} ; Processed file path: {file_url}")


