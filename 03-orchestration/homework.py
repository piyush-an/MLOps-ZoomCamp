import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import IntervalSchedule, CronSchedule
from prefect.flow_runners import SubprocessFlowRunner
from datetime import timedelta
import pickle
import os


@task
def read_data(path):
    logger = get_run_logger()
    df = pd.read_parquet(path)
    return df


@task
def prepare_features(df, categorical, train=True):
    logger = get_run_logger()
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        # print(f"The mean duration of training is {mean_duration}")
        logger.info(f"The mean duration of training is {mean_duration}")
    else:
        # print(f"The mean duration of validation is {mean_duration}")
        logger.info(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


@task
def train_model(df, categorical):
    logger = get_run_logger()
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    # print(f"The shape of X_train is {X_train.shape}")
    # print(f"The DictVectorizer has {len(dv.feature_names_)} features")

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    # print(f"The MSE of training is: {mse}")
    logger.info(f"The MSE of training is: {mse}")
    return lr, dv

@task
def run_model(df, categorical, dv, lr):
    logger = get_run_logger()
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    # print(f"The MSE of validation is: {mse}")
    logger.info(f"The MSE of validation is: {mse}")
    return

# def main(train_path: str = '../data/fhv_tripdata_2021-01.parquet', 
#            val_path: str = '../data/fhv_tripdata_2021-02.parquet'):

@flow(task_runner=SequentialTaskRunner)
# def main(user_date=None):
def main(user_date="2021-03-15"):
    logger = get_run_logger()
    if not user_date:
        user_date = date.today()
        train_date=user_date - relativedelta(months=2)
        val_date=user_date - relativedelta(months=1)
    else:
        user_date = datetime.strptime(user_date, '%Y-%m-%d')
        train_date=user_date - relativedelta(months=2)
        val_date=user_date - relativedelta(months=1)
    
    user_date = user_date.strftime("%Y-%m-%d")
    logger.info(f"Flow running for date {user_date}")

    train_date=train_date.strftime("%Y-%m")
    val_date=val_date.strftime("%Y-%m")
    train_path=f"../data/fhv_tripdata_{train_date}.parquet"
    val_path=f"../data/fhv_tripdata_{val_date}.parquet"

    if not os.path.exists(train_path):
        logger.warning(f"Training file not found, Check file at {train_path}")
        exit(101)
    
    if not os.path.exists(val_path):
        logger.warning(f"Validation file not found, Check file at {val_path}")
        exit(101)

    logger.info(f"Training and Validation file found")

    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical, False)

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()
    run_model(df_val_processed, categorical, dv, lr)

    with open(f"/home/mlops_zoomcamp/Notebooks/week03/model/model-{user_date}.bin", 'wb') as m_out:
        pickle.dump((dv, lr), m_out)
    
    with open(f"/home/mlops_zoomcamp/Notebooks/week03/model/dv-{user_date}.b", 'wb') as d_out:
        pickle.dump((dv), d_out)




# main()
# main(user_date="2021-08-15")

DeploymentSpec(
    flow=main,
    name="monthly_15_model_training",
    # schedule=IntervalSchedule(interval=timedelta(minutes=5)),
    schedule=CronSchedule(
        cron="0 9 15 * *",
        timezone="America/New_York"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml","scheduled"]
)
