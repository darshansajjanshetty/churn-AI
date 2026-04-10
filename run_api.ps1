# Activate venv and run uvicorn for FastAPI (api.py)
if (Test-Path -Path .\.venv\Scripts\Activate.ps1) {
    Write-Host "Activating virtualenv"
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Create one with: python -m venv .venv"
    exit 1
}

# Run uvicorn against api:app
uvicorn api:app --reload --host 127.0.0.1 --port 8000
