import requests

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

try:
    r = requests.post("http://127.0.0.1:8000/predict", json=sample, timeout=10)
    print('STATUS:', r.status_code)
    try:
        print('BODY:', r.json())
    except Exception:
        print('BODY (raw):', r.text)
    r.raise_for_status()
except Exception as e:
    print('ERROR:', repr(e))
