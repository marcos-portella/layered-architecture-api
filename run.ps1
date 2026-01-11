[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Clear-Host
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host " DOCKER: Gerenciando a Infraestrutura..." -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Cyan

# Write-Host "> Fazendo faxina nos containers..." -ForegroundColor Gray
# docker-compose down -v --remove-orphans

Write-Host "> Ligando os motores (API + Banco)..." -ForegroundColor Yellow
docker-compose up --build -d

Write-Host "> Aguardando MySQL ficar saudavel..." -ForegroundColor Cyan
do {
    $status = docker inspect --format='{{.State.Health.Status}}' layered_mysql_db 2>$null
    Write-Host "." -NoNewline -ForegroundColor Gray
    Start-Sleep -Seconds 2
} until ($status -eq "healthy")

Write-Host "`n[OK] TUDO PRONTO!" -ForegroundColor Green
Write-Host "-----------------------------------------------------"
Write-Host "API: http://localhost:8000"
Write-Host "Docs: http://localhost:8000/docs"
Write-Host "-----------------------------------------------------"
Write-Host "Dica: Use docker-compose logs -f para ver os logs."
