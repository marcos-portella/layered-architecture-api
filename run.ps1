. .\.venv\Scripts\Activate.ps1

Write-Host "Iniciando a API no modo Reload..." -ForegroundColor Green
uvicorn app.main:app --reload