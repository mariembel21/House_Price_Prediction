from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import numpy as np
import pandas as pd
import pickle
from pydantic import Field

import mlflow
mlflow.set_tracking_uri("sqlite:///Notebooks/mlflow.db")
app = FastAPI(title="House Price Predictor")

# Load the latest Production model from MLflow Model Registry
MODEL_NAME = "HousePriceModel"
MODEL_STAGE = "Production"
FEATURE_ARTIFACT_PATH = "model_artifacts/best_model_features.pkl"
BEST_RUN_ID = "ece9af47030f477f86d852e3e238f202"
#Load Model
model = mlflow.pyfunc.load_model(f"runs:/{BEST_RUN_ID}/model")

# Get the latest production run id (in order to get its features artifact)
client = mlflow.tracking.MlflowClient()
latest_versions = client.get_latest_versions(MODEL_NAME, stages=[MODEL_STAGE])
prod_version = latest_versions[0].version
prod_run_id = latest_versions[0].run_id

# Download artifact and load feature columns
artifact_local_path = mlflow.artifacts.download_artifacts(
    run_id=prod_run_id,
    artifact_path=FEATURE_ARTIFACT_PATH
)

with open(artifact_local_path, "rb") as f:
    feature_columns = pickle.load(f)

# If it’s a string, convert to list
if isinstance(feature_columns, str):
    import ast
    feature_columns = ast.literal_eval(feature_columns)

# Human-friendly input
class HouseFeatures(BaseModel):
    surface: float = Field(..., gt=10, lt=2000)
    rooms: int = Field(..., ge=1, le=20)
    governorate: str
    property_type: str


@app.post("/predict")
def predict_house(data: HouseFeatures):
        # Convert input to DataFrame
        df_input = pd.DataFrame([data.model_dump()])

        #Feature engineering
        df_input["rooms_per_surface"] = df_input["rooms"] / df_input["surface"]
        df_input["surface_squared"] = df_input["surface"] ** 2
        
        # One-hot encode categorical columns 
        df_input = pd.get_dummies(df_input, columns=["governorate", "property_type"], drop_first=False)

        # Align with training columns exactly
        df_input = df_input.reindex(columns=feature_columns, fill_value=0)
        
        print(df_input[feature_columns])

        # Make prediction
        pred_log_price = model.predict(df_input)
        pred_price = np.expm1(pred_log_price[0])
        
        return {"predicted_log_price": float(pred_log_price[0]),
                "predicted_price": float(pred_price)}
    
@app.get("/health")
def health():
    return {"status": "ok"}