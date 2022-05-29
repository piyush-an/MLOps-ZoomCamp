
# What is Experiment Tracking
Experiment tracking is the process of saving all experiment related information that you care about for every experiment you run.

# Why we need it?
* Reproducibility - visiting past scenario
* Organization - team collaboration
* Optimization

# Why not Spreadsheets?
Spreadsheets can be error prone, too laborious to feed all parameters, no standard template to track experiments.

# MLflow
[MLflow](https://mlflow.org/) is an open-source platform to manage the ML lifecycle, including experimentation, reproducibility, deployment, and a central model registry.

This can record,
* Parameters - dataset path, preprocessing
* Metric - accuracy
* Metadata - tags example algo name
* Artifacts - visualization
* Model - build models can be stored in a repo
* Logs additional information version number, git commits

# Installation

Create a python virtual environment,
```bash
conda create -n exp_tracking_demo python=3.9
```
Activate the `exp_tracking_demo` environment,
```bash
conda activate exp_tracking_demo
```
List all the packages in the `requirements.txt` file

```plaintext
mlflow
jupyter
scikit-learn
pandas
seaborn
hyperopt
xgboost
fastparquet
boto3
```

Install the dependency packages,
```bash
pip install -r requirements.txt
```

View the installed packages,
```bash
pip list
```

Launch mlflow dashboard and enable port forwarding in VS code `5000`
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
