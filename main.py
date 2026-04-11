"""api.py
FastAPI app that loads churn_model.pkl if present and serves predictions.
Run with: uvicorn api:app --reload --host 127.0.0.1 --port 8000
"""
import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="ChurnAI - Customer Churn Prediction")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "churn_model.pkl"

# Try to load pre-trained model if it exists
try:
    api_model = joblib.load(MODEL_PATH)
except Exception:
    api_model = None


@app.get("/")
def health_check():
    return {"message": "ChurnAI API is running", "model_loaded": api_model is not None}


@app.post("/predict")
def predict_churn(data: CustomerData):
    if api_model is None:
        raise HTTPException(status_code=503, detail="Model not available. Train the model by running `python train.py`.")

    df_input = pd.DataFrame([data.dict()])
    proba = api_model.predict_proba(df_input)[0][1]
    prediction = "Likely to Churn" if proba > 0.5 else "Not Likely to Churn"
    recommendation = "Offer retention discount or personalized plan" if proba > 0.5 else "No action needed"
    return {"churn_probability": round(proba, 2),
            "prediction": prediction,
            "recommendation": recommendation}


@app.post("/reload")
def reload_model():
    """Reload the model from disk. Returns 200 on success or 500 on failure."""
    global api_model
    try:
        api_model = joblib.load(MODEL_PATH)
        return {"detail": "Model reloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload model: {e}")
