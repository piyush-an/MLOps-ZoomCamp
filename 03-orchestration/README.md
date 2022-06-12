# Model Orchestration

## [Prefect](https://www.prefect.io/)

Prefect is a workflow management system, designed for modern infrastructure and powered by the open-source Prefect Core workflow engine. Users organize `Tasks` into `Flows`, and Prefect takes care of the rest.


![Dasboard](/images/p_dashboard.png)

## Overview of the enhancements

### 01. Decorate function with flow and task

```python
@flow(task_runner=SequentialTaskRunner)
def main(user_date="2021-03-15"):
...
@task
def prepare_features(df, categorical, train=True):
```

### 02. Enable logger
```python
logger = get_run_logger()
logger.info(f"Flow running for date {user_date}")
logger.warning(f"Training file not found, Check file at {train_path}")
```

### 03. Configure datetime to find relative train and val dataset
```python
if not user_date:
    user_date = date.today()
    train_date=user_date - relativedelta(months=2)
    val_date=user_date - relativedelta(months=1)
else:
    user_date = datetime.strptime(user_date, '%Y-%m-%d')
    train_date=user_date - relativedelta(months=2)
    val_date=user_date - relativedelta(months=1)
```

### 04. Enable logger and comment print statements
```python
logger = get_run_logger()
logger.info(f"Flow running for date {user_date}")
logger.warning(f"Training file not found, Check file at {train_path}")
```


### 05. Validate if file/path is present
```python
if not os.path.exists(train_path):
    logger.warning(f"Training file not found, Check file at {train_path}")
    exit(101)

if not os.path.exists(val_path):
    logger.warning(f"Validation file not found, Check file at {val_path}")
    exit(101)
```

### 06. Configure deployment
```python
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
```
![Scheduled Runs](/images/p_deploy.png)
Scheduled runs

# Ends
