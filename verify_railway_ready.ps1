# Script de verificación para Railway - Sin dependencias pesadas
Write-Host "=== VERIFICACIÓN PARA RAILWAY ===" -ForegroundColor Cyan
Write-Host ""

# Verificar que requirements.txt NO existe
Write-Host "1. Verificando que requirements.txt NO existe..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "❌ ERROR: requirements.txt existe. Debe ser renombrado a requirements-full.txt" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ requirements.txt NO existe" -ForegroundColor Green
}

# Verificar que requirements-prod.txt existe
Write-Host "2. Verificando requirements-prod.txt..." -ForegroundColor Yellow
if (Test-Path "requirements-prod.txt") {
    Write-Host "✅ requirements-prod.txt existe" -ForegroundColor Green
    
    # Verificar contenido
    $content = Get-Content "requirements-prod.txt"
    Write-Host "   Contenido:" -ForegroundColor White
    foreach ($line in $content) {
        Write-Host "   - $line" -ForegroundColor Gray
    }
    
    # Verificar que NO contenga dependencias pesadas
    $heavy_deps = @("torch", "tensorflow", "spacy", "transformers", "nltk", "scikit-learn", "pandas", "numpy")
    $found_heavy = @()
    
    foreach ($dep in $heavy_deps) {
        if ($content -match $dep) {
            $found_heavy += $dep
        }
    }
    
    if ($found_heavy.Count -gt 0) {
        Write-Host "❌ ADVERTENCIA: Se encontraron dependencias pesadas:" -ForegroundColor Red
        foreach ($dep in $found_heavy) {
            Write-Host "   - $dep" -ForegroundColor Red
        }
    } else {
        Write-Host "✅ No se encontraron dependencias pesadas" -ForegroundColor Green
    }
} else {
    Write-Host "❌ ERROR: requirements-prod.txt NO existe" -ForegroundColor Red
    exit 1
}

# Verificar Dockerfile
Write-Host "3. Verificando Dockerfile..." -ForegroundColor Yellow
if (Test-Path "Dockerfile") {
    Write-Host "✅ Dockerfile existe" -ForegroundColor Green
    
    $dockerfile = Get-Content "Dockerfile"
    $uses_prod = $false
    $uses_full = $false
    
    foreach ($line in $dockerfile) {
        if ($line -match "requirements-prod.txt") {
            $uses_prod = $true
        }
        if ($line -match "requirements.txt") {
            $uses_full = $true
        }
    }
    
    if ($uses_prod) {
        Write-Host "✅ Dockerfile usa requirements-prod.txt" -ForegroundColor Green
    } else {
        Write-Host "❌ ERROR: Dockerfile NO usa requirements-prod.txt" -ForegroundColor Red
    }
    
    if ($uses_full) {
        Write-Host "❌ ERROR: Dockerfile usa requirements.txt (NO DEBE)" -ForegroundColor Red
    } else {
        Write-Host "✅ Dockerfile NO usa requirements.txt" -ForegroundColor Green
    }
} else {
    Write-Host "❌ ERROR: Dockerfile NO existe" -ForegroundColor Red
    exit 1
}

# Verificar .dockerignore
Write-Host "4. Verificando .dockerignore..." -ForegroundColor Yellow
if (Test-Path ".dockerignore") {
    Write-Host "✅ .dockerignore existe" -ForegroundColor Green
    
    $dockerignore = Get-Content ".dockerignore"
    $ignores_requirements = $false
    
    foreach ($line in $dockerignore) {
        if ($line -match "requirements.txt") {
            $ignores_requirements = $true
        }
    }
    
    if ($ignores_requirements) {
        Write-Host "✅ .dockerignore ignora requirements.txt" -ForegroundColor Green
    } else {
        Write-Host "❌ ADVERTENCIA: .dockerignore NO ignora requirements.txt" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ ERROR: .dockerignore NO existe" -ForegroundColor Red
    exit 1
}

# Verificar railway.json
Write-Host "5. Verificando railway.json..." -ForegroundColor Yellow
if (Test-Path "railway.json") {
    Write-Host "✅ railway.json existe" -ForegroundColor Green
    
    $railway = Get-Content "railway.json" | ConvertFrom-Json
    if ($railway.build.command) {
        Write-Host "   Build command: $($railway.build.command)" -ForegroundColor Gray
    }
    if ($railway.deploy.startCommand) {
        Write-Host "   Start command: $($railway.deploy.startCommand)" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠️  railway.json NO existe (opcional)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== RESUMEN ===" -ForegroundColor Cyan
Write-Host "✅ Proyecto listo para Railway sin dependencias pesadas" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Pasos finales en Railway:" -ForegroundColor Yellow
Write-Host "1. Ve a Settings > Deployments" -ForegroundColor White
Write-Host "2. Activa 'Use Dockerfile (disable Nixpacks)'" -ForegroundColor White
Write-Host "3. Haz 'Clear cache' y 'Redeploy'" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Resultado esperado:" -ForegroundColor Yellow
Write-Host "- Imagen < 1GB (vs 6.8GB anterior)" -ForegroundColor White
Write-Host "- Solo dependencias esenciales instaladas" -ForegroundColor White
Write-Host "- Modelos ML descargados dinámicamente" -ForegroundColor White 