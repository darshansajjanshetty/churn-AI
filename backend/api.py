import joblib
import pandas as pd
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Churn Prediction API")

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "churn_model.pkl"
if not MODEL_PATH.exists():
    MODEL_PATH = BASE_DIR.parent / "churn_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception:
    model = None


@app.get("/")
def health_check():
    return {"message": "Churn Prediction API is running", "model_loaded": model is not None}


class Customer(BaseModel):
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


@app.post("/predict")
def predict(data: Customer):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available. Train the model or place churn_model.pkl in the backend folder.")

    df = pd.DataFrame([data.dict()])

    prob = model.predict_proba(df)[0][1]

    prediction = "Likely to Churn" if prob > 0.5 else "Not Likely to Churn"

    return {
        "churn_probability": round(prob, 2),
        "prediction": prediction
    }
