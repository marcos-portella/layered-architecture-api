# Configura o terminal para aceitar e exibir caracteres especiais (UTF-8)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Clear-Host
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  DOCKER QA: Rodando testes dentro do container..." -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Cyan

# Executa o pytest DENTRO do container da API que já está rodando
# 'exec' roda o comando no container ativo
# '-T' remove a necessidade de um terminal interativo (melhor para automação)
docker exec -it layered_fastapi_app python -m pytest --cov=app tests/ --cov-report=term-missing --cov-fail-under=100 --cache-clear

# Verifica o resultado final do comando dentro do Docker
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[X] Ops! Testes falharam ou cobertura menor que 100% no Docker." -ForegroundColor Red
} else {
    Write-Host "`n[OK] SUCESSO! Ambiente isolado, blindado e 100% testado." -ForegroundColor Green
}