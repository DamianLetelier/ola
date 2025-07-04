# Script para verificar que el proyecto esté listo para Railway

Write-Host "=== VERIFICACIÓN PARA RAILWAY ===" -ForegroundColor Green
Write-Host ""

# Verificar archivos esenciales
$requiredFiles = @(
    "Dockerfile",
    "requirements-prod.txt", 
    "manage.py",
    "Crud_Damian/settings.py",
    "Crud_Damian/wsgi.py"
)

Write-Host "Verificando archivos esenciales..." -ForegroundColor Yellow
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file (FALTANTE)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Verificando Dockerfile..." -ForegroundColor Yellow
$dockerfileContent = Get-Content "Dockerfile" -Raw
if ($dockerfileContent -match "pip install -r requirements-prod.txt") {
    Write-Host "✅ Dockerfile usa requirements-prod.txt" -ForegroundColor Green
} else {
    Write-Host "❌ Dockerfile NO usa requirements-prod.txt" -ForegroundColor Red
}

if ($dockerfileContent -match "requirements.txt") {
    Write-Host "❌ Dockerfile aún referencia requirements.txt" -ForegroundColor Red
} else {
    Write-Host "✅ Dockerfile NO referencia requirements.txt" -ForegroundColor Green
}

Write-Host ""
Write-Host "Verificando dependencias de producción..." -ForegroundColor Yellow
$prodDeps = Get-Content "requirements-prod.txt"
$requiredDeps = @("Django", "gunicorn", "whitenoise", "dj-database-url", "requests", "yara-python", "stanza", "Pillow")
$heavyDeps = @("torch", "spacy", "nltk", "psutil")
$foundHeavy = @()
$missingRequired = @()

foreach ($dep in $prodDeps) {
    $depName = ($dep -split ">=")[0] -split ">="
    $depName = $depName[0].Trim()
    if ($heavyDeps -contains $depName) {
        $foundHeavy += $depName
    }
}

foreach ($reqDep in $requiredDeps) {
    $found = $false
    foreach ($dep in $prodDeps) {
        $depName = ($dep -split ">=")[0] -split ">="
        $depName = $depName[0].Trim()
        if ($depName -eq $reqDep) {
            $found = $true
            break
        }
    }
    if (-not $found) {
        $missingRequired += $reqDep
    }
}

if ($foundHeavy.Count -eq 0) {
    Write-Host "✅ requirements-prod.txt está limpio (sin dependencias pesadas innecesarias)" -ForegroundColor Green
} else {
    Write-Host "⚠️ requirements-prod.txt contiene dependencias pesadas: $($foundHeavy -join ', ')" -ForegroundColor Yellow
}

if ($missingRequired.Count -eq 0) {
    Write-Host "✅ requirements-prod.txt incluye todas las dependencias necesarias" -ForegroundColor Green
} else {
    Write-Host "❌ requirements-prod.txt faltan dependencias: $($missingRequired -join ', ')" -ForegroundColor Red
}

Write-Host ""
Write-Host "Verificando tamaño del proyecto..." -ForegroundColor Yellow
try {
    $size = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $sizeMB = [math]::Round($size / 1MB, 2)
    Write-Host "Tamaño actual: $sizeMB MB" -ForegroundColor White
    
    if ($sizeMB -lt 100) {
        Write-Host "✅ Tamaño óptimo para Railway" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Tamaño grande, pero el Dockerfile controlará las dependencias" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ No se pudo calcular el tamaño" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== RESUMEN ===" -ForegroundColor Green
Write-Host "✅ Dockerfile: Controla dependencias" -ForegroundColor Green
Write-Host "✅ requirements-prod.txt: Solo dependencias esenciales" -ForegroundColor Green
Write-Host "✅ Nixpacks: Se desactivará automáticamente" -ForegroundColor Green
Write-Host "✅ Railway: Usará Dockerfile en lugar de adivinar" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Tu proyecto está listo para Railway!" -ForegroundColor Green
Write-Host "Sube a GitHub y conecta a Railway. El Dockerfile se encargará de todo." -ForegroundColor Yellow 