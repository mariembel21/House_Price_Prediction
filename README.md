#  House Price Prediction in Tunisia

Machine learning project for predicting house prices in Tunisia using real-estate listing data.

The project covers data preparation, exploratory analysis, machine learning model training, experiment tracking with MLflow, and prediction serving through a FastAPI API.

---


## Project Structure


```text
House-Price-Prediction/
│
├── data/
│
├── HouseScraper/
│
├── Notebooks/
│   ├── artifacts/
│   ├── mlruns/
│   └── 1_data_preprocessing.ipynb
│
├── fastapi_app.py
├── mlflow.db
├── requirements.txt
├── requirements-prod.txt
├── .gitignore
└── README.md
```

---

## Project Workflow

1.Collect real-estate listing data
2.Clean and preprocess the data
3.Explore the main features and price distribution
4.Prepare features for machine learning
5.Train and evaluate regression models
6.Track experiments and models with MLflow
7.Serve predictions through FastAPI

---

## Data

The dataset is based on real-estate listings from Tunisian property platforms.

The main features include:

price
surface
rooms
governorate
property_type

The data is cleaned and transformed before being used for model training.

---

## Machine Learning

The project evaluates regression models for house price prediction.

Feature preparation includes:

Handling missing and invalid values
Numerical transformations
Feature engineering
Encoding categorical variables
Preparing the final dataset for model training

The target variable is the property price.

---

## Experiment Tracking

MLflow is used to track machine learning experiments.

It allows the project to keep track of:

Model parameters
Evaluation metrics
Model artifacts
Experiment runs

The local MLflow tracking database and experiment artifacts are stored in the repository.



---


