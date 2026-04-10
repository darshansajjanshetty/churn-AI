"""dashboard.py
Streamlit dashboard that posts to the FastAPI prediction endpoint.
Run with: streamlit run dashboard.py
"""
import streamlit as st
import requests


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
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=customer_data)
            result = response.json()
            st.write(result)
        except Exception as e:
            st.error(f"Error calling API: {e}")


if __name__ == '__main__':
    run_dashboard()
