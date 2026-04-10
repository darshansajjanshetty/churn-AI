import { useState } from "react";
import "./PredictionForm.css";

const PredictionForm = ({ onPredict, loading }) => {
  const [formData, setFormData] = useState({
    gender: "Male",
    SeniorCitizen: 0,
    Partner: "Yes",
    Dependents: "No",
    tenure: 12,
    PhoneService: "Yes",
    MultipleLines: "No",
    InternetService: "Fiber optic",
    OnlineSecurity: "No",
    OnlineBackup: "No",
    DeviceProtection: "No",
    TechSupport: "No",
    StreamingTV: "No",
    StreamingMovies: "No",
    Contract: "Month-to-month",
    PaperlessBilling: "Yes",
    PaymentMethod: "Electronic check",
    MonthlyCharges: 65.0,
    TotalCharges: 780.0,
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? parseFloat(value) : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(formData);
  };

  const handleReset = () => {
    setFormData({
      gender: "Male",
      SeniorCitizen: 0,
      Partner: "Yes",
      Dependents: "No",
      tenure: 12,
      PhoneService: "Yes",
      MultipleLines: "No",
      InternetService: "Fiber optic",
      OnlineSecurity: "No",
      OnlineBackup: "No",
      DeviceProtection: "No",
      TechSupport: "No",
      StreamingTV: "No",
      StreamingMovies: "No",
      Contract: "Month-to-month",
      PaperlessBilling: "Yes",
      PaymentMethod: "Electronic check",
      MonthlyCharges: 65.0,
      TotalCharges: 780.0,
    });
  };

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <h2>Customer Information</h2>

      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="gender">Gender</label>
          <select
            id="gender"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            disabled={loading}
          >
            <option>Male</option>
            <option>Female</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="SeniorCitizen">Senior Citizen</label>
          <select
            id="SeniorCitizen"
            name="SeniorCitizen"
            value={formData.SeniorCitizen}
            onChange={handleChange}
            disabled={loading}
          >
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="Partner">Partner</label>
          <select
            id="Partner"
            name="Partner"
            value={formData.Partner}
            onChange={handleChange}
            disabled={loading}
          >
            <option>Yes</option>
            <option>No</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="Dependents">Dependents</label>
          <select
            id="Dependents"
            name="Dependents"
            value={formData.Dependents}
            onChange={handleChange}
            disabled={loading}
          >
            <option>Yes</option>
            <option>No</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="tenure">Tenure (months)</label>
          <input
            type="number"
            id="tenure"
            name="tenure"
            min="0"
            max="72"
            value={formData.tenure}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="MonthlyCharges">Monthly Charges ($)</label>
          <input
            type="number"
            id="MonthlyCharges"
            name="MonthlyCharges"
            min="0"
            step="0.01"
            value={formData.MonthlyCharges}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="TotalCharges">Total Charges ($)</label>
          <input
            type="number"
            id="TotalCharges"
            name="TotalCharges"
            min="0"
            step="0.01"
            value={formData.TotalCharges}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="PhoneService">Phone Service</label>
          <select
            id="PhoneService"
            name="PhoneService"
            value={formData.PhoneService}
            onChange={handleChange}
            disabled={loading}
          >
            <option>Yes</option>
            <option>No</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="InternetService">Internet Service</label>
          <select
            id="InternetService"
            name="InternetService"
            value={formData.InternetService}
            onChange={handleChange}
            disabled={loading}
          >
            <option>Fiber optic</option>
            <option>DSL</option>
            <option>No</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="Contract">Contract Type</label>
          <select
            id="Contract"
            name="Contract"
            value={formData.Contract}
            onChange={handleChange}
            disabled={loading}
          >
            <option>Month-to-month</option>
            <option>One year</option>
            <option>Two year</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="OnlineSecurity">Online Security</label>
          <select
            id="OnlineSecurity"
            name="OnlineSecurity"
            value={formData.OnlineSecurity}
            onChange={handleChange}
            disabled={loading}
          >
            <option>No</option>
            <option>Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="TechSupport">Tech Support</label>
          <select
            id="TechSupport"
            name="TechSupport"
            value={formData.TechSupport}
            onChange={handleChange}
            disabled={loading}
          >
            <option>No</option>
            <option>Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="PaperlessBilling">Paperless Billing</label>
          <select
            id="PaperlessBilling"
            name="PaperlessBilling"
            value={formData.PaperlessBilling}
            onChange={handleChange}
            disabled={loading}
          >
            <option>Yes</option>
            <option>No</option>
          </select>
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn-predict" disabled={loading}>
          {loading ? "Analyzing..." : "🔮 Predict Churn"}
        </button>
        <button
          type="button"
          className="btn-reset"
          onClick={handleReset}
          disabled={loading}
        >
          Reset
        </button>
      </div>
    </form>
  );
};

export default PredictionForm;
