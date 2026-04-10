import os
import pytest
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


@pytest.mark.skipif(not os.path.exists('churn_model.pkl'), reason='Model file churn_model.pkl not found')
def test_reload_and_predict():
    # Reload model
    r = client.post('/reload')
    assert r.status_code == 200

    # Minimal sample - these keys must match the model's expected fields
    sample = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 1,
        "PhoneService": "No",
        "MultipleLines": "No phone service",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 29.85,
        "TotalCharges": 29.85
    }

    r2 = client.post('/predict', json=sample)
    assert r2.status_code == 200
    data = r2.json()
    assert 'churn_probability' in data and 'prediction' in data and 'recommendation' in data
