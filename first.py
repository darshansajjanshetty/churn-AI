# churnai_project.py
"""
ChurnAI – Predicting Customer Churn using Behavioral Analytics
Complete Python Project: Preprocessing, Model, API, Dashboard
"""

# =========================
# Step 0: Import Libraries
# =========================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import streamlit as st
import requests

# NOTE: Training code moved into `if __name__ == '__main__'` below so importing
# this module (for example by `uvicorn first:app`) doesn't retrain the model.
# At module import time we only attempt to load an existing saved model.

# Placeholder pipeline and model variables (will be set when training)
pipeline = None

# Try to load pre-trained model if it exists
try:
    api_model = joblib.load("churn_model.pkl")
except Exception:
    api_model = None

# =========================
# Step 3: FastAPI Deployment
# =========================
app = FastAPI(title="ChurnAI - Customer Churn Prediction")

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

@app.post("/predict")
def predict_churn(data: CustomerData):
    """Predict churn for a single customer. Returns 503 if model not loaded."""
    if api_model is None:
        return {"detail": "Model not available. Train the model by running `python first.py`."}, 503

    df_input = pd.DataFrame([data.dict()])
    probability = api_model.predict_proba(df_input)[0][1]
    prediction = "Likely to Churn" if probability > 0.5 else "Not Likely to Churn"
    recommendation = "Offer retention discount or personalized plan" if probability > 0.5 else "No action needed"
    return {"churn_probability": round(probability, 2),
            "prediction": prediction,
            "recommendation": recommendation}

# =========================
# Step 4: Streamlit Dashboard (Optional)
# =========================
def run_dashboard():
    st.title("ChurnAI Dashboard")
    st.header("Enter Customer Details")

    customer_data = {
        "gender": st.selectbox("Gender", ["Male", "Female"]),
        "SeniorCitizen": st.number_input("SeniorCitizen", 0, 1),
        "Partner": st.selectbox("Partner", ["Yes","No"]),
        "Dependents": st.selectbox("Dependents", ["Yes","No"]),
        "tenure": st.number_input("Tenure (months)", 0, 72),
        "PhoneService": st.selectbox("PhoneService", ["Yes","No"]),
        "MultipleLines": st.selectbox("MultipleLines", ["Yes","No","No phone service"]),
        "InternetService": st.selectbox("InternetService", ["DSL","Fiber optic","No"]),
        "OnlineSecurity": st.selectbox("OnlineSecurity", ["Yes","No","No internet service"]),
        "OnlineBackup": st.selectbox("OnlineBackup", ["Yes","No","No internet service"]),
        "DeviceProtection": st.selectbox("DeviceProtection", ["Yes","No","No internet service"]),
        "TechSupport": st.selectbox("TechSupport", ["Yes","No","No internet service"]),
        "StreamingTV": st.selectbox("StreamingTV", ["Yes","No","No internet service"]),
        "StreamingMovies": st.selectbox("StreamingMovies", ["Yes","No","No internet service"]),
        "Contract": st.selectbox("Contract", ["Month-to-month","One year","Two year"]),
        "PaperlessBilling": st.selectbox("PaperlessBilling", ["Yes","No"]),
        "PaymentMethod": st.selectbox("PaymentMethod", ["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"]),
        "MonthlyCharges": st.number_input("MonthlyCharges", 0.0, 500.0),
        "TotalCharges": st.number_input("TotalCharges", 0.0, 20000.0)
    }

    if st.button("Predict Churn"):
        response = requests.post("http://127.0.0.1:8000/predict", json=customer_data)
        result = response.json()
        st.write(result)

# Uncomment to run Streamlit dashboard
# if __name__ == "__main__":
#     run_dashboard()


if __name__ == '__main__':
    # =========================
    # Step 1: Data Preprocessing
    # =========================
    # Load dataset
    df = pd.read_csv("Telco-Customer-Churn.csv")

    # Drop unnecessary columns
    if 'customerID' in df.columns:
        df.drop('customerID', axis=1, inplace=True)

    # Convert TotalCharges to numeric
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

    # Encode target
    if 'Churn' in df.columns:
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    else:
        raise RuntimeError('Dataset must contain a Churn column')

    # Identify categorical and numerical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    # Remove target if it's in numerical_cols
    if 'Churn' in numerical_cols:
        numerical_cols.remove('Churn')  # remove target

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(drop='first', sparse=False), categorical_cols)
    ])

    # Split data
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

    # Handle class imbalance
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    # =========================
    # Step 2: Model Training
    # =========================
    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    # Train
    pipeline.fit(X_train_res, y_train_res)

    # Validation
    y_pred = pipeline.predict(X_val)
    y_proba = pipeline.predict_proba(X_val)[:, 1]

    print("Classification Report:\n", classification_report(y_val, y_pred))
    print("ROC-AUC Score:", roc_auc_score(y_val, y_proba))

    # Save trained model
    joblib.dump(pipeline, "churn_model.pkl")
    print('Model trained and saved to churn_model.pkl')
