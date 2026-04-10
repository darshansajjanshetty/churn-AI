# ChurnAI - Customer Churn Prediction System

A machine learning application that predicts customer churn using a Random Forest classifier, with a FastAPI backend and React frontend.

## Project Structure

```
churn-ai-project/
│
├── backend/
│   ├── train.py                 # Model training script
│   ├── api.py                   # FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── Telco-Customer-Churn.csv # Dataset
│   └── churn_model.pkl          # Trained model (generated after training)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # React main component
│   │   ├── App.css              # Styling
│   │   ├── main.jsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
└── README.md                    # This file
```

## Architecture

```
React Frontend (http://localhost:5173)
         ↓
FastAPI Backend (http://127.0.0.1:8000)
         ↓
ML Model (RandomForest)
         ↓
Predictions
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm

### 1. Backend Setup

#### Navigate to backend directory:

```bash
cd backend
```

#### Create and activate virtual environment:

```bash
python -m venv venv
```

**On Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

#### Install dependencies:

```bash
pip install -r requirements.txt
```

**Note:** Ensure `Telco-Customer-Churn.csv` is in the `backend/` directory before training.

#### Train the model:

```bash
python train.py
```

This will:

- Read `Telco-Customer-Churn.csv`
- Train a Random Forest classifier with SMOTE oversampling
- Display validation metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
- Save the model as `churn_model.pkl`

#### Start the FastAPI server:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at: **http://127.0.0.1:8000**

**API Documentation:** http://127.0.0.1:8000/docs

### 2. Frontend Setup

#### Open a new terminal and navigate to frontend directory:

```bash
cd frontend
```

#### Install dependencies:

```bash
npm install
```

#### Start the development server:

```bash
npm run dev
```

The frontend will be available at: **http://localhost:5173**

## Usage

1. **Start the backend** (as described above)
2. **Start the frontend** (in a new terminal)
3. **Open** http://localhost:5173 in your browser
4. **Fill in customer information**
5. **Click "Predict"** to get churn prediction

## Features

### Input Fields

- **Tenure** (months): Customer account duration
- **Monthly Charges** ($): Monthly subscription cost
- **Total Charges** ($): Total amount spent
- **Gender**: Male / Female
- **Senior Citizen**: Yes / No
- **Partner Status**: Yes / No
- **Internet Service**: DSL / Fiber optic / None
- **Contract Type**: Month-to-month / One year / Two year

### Output

- **Churn Probability**: Likelihood of customer leaving (0-1 or 0-100%)
- **Prediction**: "Likely to Churn" or "Not Likely to Churn"

## Model Details

### Algorithm

- **Classifier**: Random Forest (200 trees)
- **Preprocessing**:
  - Standard Scaling for numerical features
  - One-Hot Encoding for categorical features
- **Handle Imbalance**: SMOTE oversampling
- **Train-Test Split**: 80-20

### Expected Performance

- Accuracy: ~80%
- Precision: High specificity for churn detection
- Recall: Good sensitivity to actually churning customers
- ROC-AUC: Strong discrimination ability

## API Endpoints

### GET /

Health check endpoint

```bash
curl http://127.0.0.1:8000/
```

### POST /predict

Predict churn for a customer

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 10,
    "PhoneService": "Yes",
    "MultipleLines": "No",
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
    "MonthlyCharges": 50.0,
    "TotalCharges": 500.0
  }'
```

**Response:**

```json
{
  "churn_probability": 0.73,
  "prediction": "Likely to Churn"
}
```

## Common Issues

### Backend not connecting to frontend

- Ensure FastAPI server is running on `http://127.0.0.1:8000`
- Check that CORS middleware is enabled in `api.py`
- Verify firewall is not blocking port 8000

### Model file not found

- Run `python train.py` in the backend directory first
- Ensure `Telco-Customer-Churn.csv` exists in backend directory

### CSV file not found

- Place `Telco-Customer-Churn.csv` in the `backend/` directory
- Ensure the filename matches exactly (case-sensitive on Linux/macOS)

### Port already in use

- Backend: `lsof -i :8000` (macOS/Linux) or check port 8000
- Frontend: `lsof -i :5173` (macOS/Linux) or check port 5173
- Kill processes or use different ports

## Customization

### Change Backend Port

Edit `api.py` startup command:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8001
```

Update frontend API URL in `App.jsx`:

```javascript
const response = await fetch("http://127.0.0.1:8001/predict", {
  ...
});
```

### Adjust Model Parameters

Edit `train.py`:

- `n_estimators`: Number of trees in Random Forest
- `test_size`: Train-test split ratio
- `random_state`: Random seed for reproducibility

## Technologies Used

### Backend

- **Python 3.8+**
- **FastAPI**: Modern Python web framework
- **scikit-learn**: Machine learning library
- **imbalanced-learn**: SMOTE for handling imbalanced data
- **joblib**: Model serialization
- **pandas**: Data manipulation
- **uvicorn**: ASGI server

### Frontend

- **React 18**: UI framework
- **Vite**: Build tool
- **Fetch API**: HTTP requests

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions:

1. Check the Common Issues section above
2. Verify all dependencies are installed
3. Ensure the required CSV file is in the correct location
4. Check that both backend and frontend servers are running

---

**Happy Predicting!** 🎯
