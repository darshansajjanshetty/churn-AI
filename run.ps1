# ChurnAI Project Launcher
# Run with: .\run.ps1

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      ChurnAI Project Launcher          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Backend setup
Write-Host "🔧 Setting up backend..." -ForegroundColor Yellow
$backendDir = ".\backend"
$venvPath = "$backendDir\venv"

# Create venv if not exists
if (-not (Test-Path $venvPath)) {
    Write-Host "   Creating virtual environment..."
    python -m venv $venvPath
}

# Activate venv
Write-Host "   Activating virtual environment..."
& "$venvPath\Scripts\Activate.ps1"

# Install dependencies
Write-Host "   Installing dependencies..."
pip install -q -r "$backendDir\requirements.txt" 2>$null

# Train model if not exists
if (-not (Test-Path "$backendDir\churn_model.pkl")) {
    Write-Host "   Training model (this may take a minute)..." -ForegroundColor Cyan
    Set-Location $backendDir
    python train.py
    Set-Location ..
} else {
    Write-Host "   Model already trained ✓" -ForegroundColor Green
}

# Start backend
Write-Host ""
Write-Host "🚀 Starting FastAPI backend on http://127.0.0.1:8000" -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    & "$args[1]\Scripts\Activate.ps1"
    uvicorn backend.api:app --reload --host 127.0.0.1 --port 8000
} -ArgumentList (Get-Location).Path, $venvPath

# Start frontend
Write-Host "🚀 Starting React frontend on http://localhost:5173" -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    npm run dev
} -ArgumentList "$((Get-Location).Path)\frontend"

Write-Host ""
Write-Host "✅ Both servers are starting..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "📍 Backend:   http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "📍 API Docs:  http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏳ Waiting for servers to warm up (10 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "🎉 Project is running! Press Ctrl+C to stop everything." -ForegroundColor Green
Write-Host ""

# Wait for jobs
$backendJob, $frontendJob | Wait-Job
