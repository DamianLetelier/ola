# Script agresivo para limpiar archivos duplicados y innecesarios (Windows PowerShell)

Write-Host "=== LIMPIEZA AGRESIVA PARA RAILWAY ===" -ForegroundColor Green
Write-Host "Eliminando archivos duplicados y innecesarios..." -ForegroundColor Yellow

# 1. ELIMINAR CARPETAS DUPLICADAS Y INNECESARIAS
Write-Host "1. Eliminando carpetas duplicadas..." -ForegroundColor Cyan

# Eliminar la carpeta de herramientas completa (es una copia duplicada)
Write-Host "   - Eliminando herramientas/ (copia duplicada)" -ForegroundColor White
if (Test-Path "herramientas") {
    Remove-Item -Recurse -Force "herramientas" -ErrorAction SilentlyContinue
}

# Eliminar carpeta de presentación (contiene archivos grandes)
Write-Host "   - Eliminando Artefacto-8-Presentación-final/ (archivos grandes)" -ForegroundColor White
if (Test-Path "Artefacto-8-Presentación-final") {
    Remove-Item -Recurse -Force "Artefacto-8-Presentación-final" -ErrorAction SilentlyContinue
}

# Eliminar carpeta de proyecto (parece ser documentación)
Write-Host "   - Eliminando proyecto/ (documentación innecesaria)" -ForegroundColor White
if (Test-Path "proyecto") {
    Remove-Item -Recurse -Force "proyecto" -ErrorAction SilentlyContinue
}

# 2. ELIMINAR ARCHIVOS DE BASE DE DATOS
Write-Host "2. Eliminando archivos de base de datos..." -ForegroundColor Cyan
Get-ChildItem -Name "*.sqlite3" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }
Get-ChildItem -Name "*.db" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }

# 3. ELIMINAR ARCHIVOS MULTIMEDIA GRANDES
Write-Host "3. Eliminando archivos multimedia grandes..." -ForegroundColor Cyan
$mediaExtensions = @("*.mp4", "*.avi", "*.mov", "*.gif", "*.webp", "*.png", "*.jpg", "*.jpeg")
foreach ($ext in $mediaExtensions) {
    Get-ChildItem -Recurse -Name $ext -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }
}

# 4. ELIMINAR ARCHIVOS DE DOCUMENTOS
Write-Host "4. Eliminando archivos de documentos..." -ForegroundColor Cyan
$docExtensions = @("*.docx", "*.doc", "*.pdf", "*.pptx", "*.ppt")
foreach ($ext in $docExtensions) {
    Get-ChildItem -Recurse -Name $ext -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }
}

# 5. ELIMINAR ARCHIVOS DE CACHE Y TEMPORALES
Write-Host "5. Eliminando archivos de cache..." -ForegroundColor Cyan
Get-ChildItem -Recurse -Directory -Name "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Recurse -Force -ErrorAction SilentlyContinue }
Get-ChildItem -Recurse -Name "*.pyc" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }
Get-ChildItem -Recurse -Name "*.pyo" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }

# 6. ELIMINAR ARCHIVOS DE LOGS
Write-Host "6. Eliminando archivos de logs..." -ForegroundColor Cyan
Get-ChildItem -Recurse -Name "*.log" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }

# 7. ELIMINAR ARCHIVOS DE BUILD
Write-Host "7. Eliminando archivos de build..." -ForegroundColor Cyan
if (Test-Path "build") { Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue }
Get-ChildItem -Directory -Name "*egg-info" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Recurse -Force -ErrorAction SilentlyContinue }

# 8. ELIMINAR ARCHIVOS DE ENTORNO
Write-Host "8. Eliminando archivos de entorno..." -ForegroundColor Cyan
if (Test-Path "environment.yml") { Remove-Item "environment.yml" -Force -ErrorAction SilentlyContinue }
if (Test-Path ".venv") { Remove-Item -Recurse -Force ".venv" -ErrorAction SilentlyContinue }
if (Test-Path "venv") { Remove-Item -Recurse -Force "venv" -ErrorAction SilentlyContinue }
if (Test-Path "env") { Remove-Item -Recurse -Force "env" -ErrorAction SilentlyContinue }

# 9. ELIMINAR ARCHIVOS DE IDE
Write-Host "9. Eliminando archivos de IDE..." -ForegroundColor Cyan
if (Test-Path ".vscode") { Remove-Item -Recurse -Force ".vscode" -ErrorAction SilentlyContinue }
if (Test-Path ".idea") { Remove-Item -Recurse -Force ".idea" -ErrorAction SilentlyContinue }

# 10. ELIMINAR ARCHIVOS DEL SISTEMA
Write-Host "10. Eliminando archivos del sistema..." -ForegroundColor Cyan
Get-ChildItem -Recurse -Name ".DS_Store" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }
Get-ChildItem -Recurse -Name "Thumbs.db" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_ -Force -ErrorAction SilentlyContinue }

# 11. ELIMINAR CARPETA MEDIA COMPLETA (se recreará en Railway)
Write-Host "11. Eliminando carpeta media/ (se recreará en Railway)..." -ForegroundColor Cyan
if (Test-Path "media") { Remove-Item -Recurse -Force "media" -ErrorAction SilentlyContinue }

# 12. ELIMINAR ARCHIVOS DE YARA (si no son necesarios para el despliegue)
Write-Host "12. Eliminando archivos de YARA (opcional)..." -ForegroundColor Cyan
if (Test-Path "yara_rules") { Remove-Item -Recurse -Force "yara_rules" -ErrorAction SilentlyContinue }

Write-Host ""
Write-Host "=== LIMPIEZA COMPLETADA ===" -ForegroundColor Green

# Mostrar tamaño actual
Write-Host "Tamaño actual del proyecto:" -ForegroundColor Yellow
try {
    $size = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $sizeMB = [math]::Round($size / 1MB, 2)
    Write-Host "$sizeMB MB" -ForegroundColor Green
} catch {
    Write-Host "No se pudo calcular el tamaño" -ForegroundColor Red
}

Write-Host ""
Write-Host "Archivos Python restantes:" -ForegroundColor Yellow
Get-ChildItem -Recurse -Name "*.py" | Select-Object -First 10
Write-Host "..." 