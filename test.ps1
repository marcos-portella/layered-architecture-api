. .\.venv\Scripts\Activate.ps1

Clear-Host
Write-Host "Rodando testes e caçando linhas sem cobertura..." -ForegroundColor Yellow

# Roda o pytest focando no que importa para os 100%
python -m pytest --cov=app tests/ --cov-report=term-missing --cov-fail-under=100

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ops! Ou um teste falhou ou você não atingiu 100% de cobertura." -ForegroundColor Red
} else {
    Write-Host "✅ SUCESSO! Código blindado e 100% testado." -ForegroundColor Green
}