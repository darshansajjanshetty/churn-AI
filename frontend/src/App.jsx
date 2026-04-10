import React, { useState } from "react";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    gender: "Male",
    SeniorCitizen: 0,
    Partner: "Yes",
    Dependents: "No",
    tenure: 10,
    PhoneService: "Yes",
    MultipleLines: "No",
    InternetService: "DSL",
    OnlineSecurity: "No",
    OnlineBackup: "No",
    DeviceProtection: "No",
    TechSupport: "No",
    StreamingTV: "No",
    StreamingMovies: "No",
    Contract: "Month-to-month",
    PaperlessBilling: "Yes",
    PaymentMethod: "Electronic check",
    MonthlyCharges: 50,
    TotalCharges: 500,
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setForm({
      ...form,
      [name]: type === "number" ? parseFloat(value) : value,
    });
  };

  const predict = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const body = await res.text();
        throw new Error(
          `Backend returned ${res.status} ${res.statusText}: ${body}`,
        );
      }
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(
        `Error connecting to backend. Make sure the API is running on http://127.0.0.1:8000. ${err?.message || ""}`,
      );
      console.error("Prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Churn Prediction System</h1>

      <div className="form-group">
        <label>Tenure (months)</label>
        <input
          type="number"
          name="tenure"
          placeholder="Tenure"
          value={form.tenure}
          onChange={handleChange}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label>Monthly Charges ($)</label>
        <input
          type="number"
          name="MonthlyCharges"
          placeholder="Monthly Charges"
          value={form.MonthlyCharges}
          onChange={handleChange}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label>Total Charges ($)</label>
        <input
          type="number"
          name="TotalCharges"
          placeholder="Total Charges"
          value={form.TotalCharges}
          onChange={handleChange}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label>Gender</label>
        <select
          name="gender"
          value={form.gender}
          onChange={handleChange}
          disabled={loading}
        >
          <option>Male</option>
          <option>Female</option>
        </select>
      </div>

      <div className="form-group">
        <label>Senior Citizen</label>
        <select
          name="SeniorCitizen"
          value={form.SeniorCitizen}
          onChange={handleChange}
          disabled={loading}
        >
          <option value="0">No</option>
          <option value="1">Yes</option>
        </select>
      </div>

      <div className="form-group">
        <label>Partner</label>
        <select
          name="Partner"
          value={form.Partner}
          onChange={handleChange}
          disabled={loading}
        >
          <option>Yes</option>
          <option>No</option>
        </select>
      </div>

      <div className="form-group">
        <label>Internet Service</label>
        <select
          name="InternetService"
          value={form.InternetService}
          onChange={handleChange}
          disabled={loading}
        >
          <option>DSL</option>
          <option>Fiber optic</option>
          <option>No</option>
        </select>
      </div>

      <div className="form-group">
        <label>Contract</label>
        <select
          name="Contract"
          value={form.Contract}
          onChange={handleChange}
          disabled={loading}
        >
          <option>Month-to-month</option>
          <option>One year</option>
          <option>Two year</option>
        </select>
      </div>

      <button onClick={predict} disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="result">
          <h2>Prediction</h2>
          <p>
            <strong>Probability:</strong>{" "}
            {(result.churn_probability * 100).toFixed(1)}%
          </p>
          <p>
            <strong>Status:</strong> {result.prediction}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
