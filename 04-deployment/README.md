# Deployment

* Published API: https://nyc-taxi.anandpiyush.com/
* Endpoint Doc: https://nyc-taxi.anandpiyush.com/docs
  
![Homepage](/images/homepage.png)
---

# Accomplishments

1. Using a model predict the ride duration of a trip
2. Parametrize the script to take user input in the form of YYYY and MM and return the mean predicted value
   ```python
   python predict.py --year 2021 --month 04
   ```
   Output:
   ```plaintext
   Mean predict value for the year 2021 and month 04 is 16.55
   ```
3. Convert the predict.py into a app using [FastAPI](https://fastapi.tiangolo.com/) 
   1. Home page designed using simple HTML
   2. Endpoint created to API
   3. Functions for prediction, file export and upload to GCP bucket
   
4. Build as a docker container, refer branch  [deploy-app](https://github.com/piyush-an/MLOps-ZoomCamp/tree/deploy-app)
5. Enable GitActions for automated build and publish docker image to Google [Container Registry](https://cloud.google.com/container-registry)
6. Setup service accounts in GCP for public view access and write permission to bucket of processed file
7. Deploy the container image using [Cloud Run](https://cloud.google.com/run)
8. Configure subdomain
   
![API](/images/api.png)