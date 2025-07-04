# Script para instalar dependencias de desarrollo (Windows PowerShell)

Write-Host "=== INSTALANDO DEPENDENCIAS DE DESARROLLO ===" -ForegroundColor Green
Write-Host "Esto instalará todas las librerías necesarias para desarrollo local" -ForegroundColor Yellow
Write-Host "Incluyendo librerías de machine learning (Spacy, Stanza, NLTK, etc.)" -ForegroundColor Yellow
Write-Host ""

# Verificar si existe el archivo
if (Test-Path "requirements-dev.txt") {
    Write-Host "Instalando dependencias desde requirements-dev.txt..." -ForegroundColor Cyan
    pip install -r requirements-dev.txt
    
    Write-Host ""
    Write-Host "=== INSTALACIÓN COMPLETADA ===" -ForegroundColor Green
    Write-Host "Ahora puedes ejecutar la aplicación localmente:" -ForegroundColor Yellow
    Write-Host "python manage.py runserver" -ForegroundColor White
} else {
    Write-Host "ERROR: No se encontró requirements-dev.txt" -ForegroundColor Red
    Write-Host "Asegúrate de que el archivo existe en el directorio actual" -ForegroundColor Red
} 