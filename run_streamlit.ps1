# Activate venv and run Streamlit dashboard
if (Test-Path -Path .\.venv\Scripts\Activate.ps1) {
    Write-Host "Activating virtualenv"
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Create one with: python -m venv .venv"
    exit 1
}

streamlit run dashboard.py
