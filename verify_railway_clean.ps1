# Script para verificar que Railway está configurado correctamente
# y NO instalará dependencias pesadas

Write-Host "🔍 VERIFICANDO CONFIGURACIÓN PARA RAILWAY" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Verificar que requirements-prod.txt existe y es liviano
Write-Host "`n📋 Verificando requirements-prod.txt..." -ForegroundColor Yellow
if (Test-Path "requirements-prod.txt") {
    $prodContent = Get-Content "requirements-prod.txt"
    $prodSize = (Get-Item "requirements-prod.txt").Length
    
    Write-Host "✅ requirements-prod.txt existe (${prodSize} bytes)" -ForegroundColor Green
    
    # Verificar que NO contiene dependencias pesadas
    $heavyDeps = @("torch", "stanza", "yara-python", "nltk", "transformers", "numpy", "scikit-learn", "spacy")
    $foundHeavy = @()
    
    foreach ($dep in $heavyDeps) {
        foreach ($line in $prodContent) {
            if ($line -match $dep) {
                $foundHeavy += $dep
                break
            }
        }
    }
    
    if ($foundHeavy.Count -eq 0) {
        Write-Host "✅ NO contiene dependencias pesadas" -ForegroundColor Green
    } else {
        Write-Host "❌ CONTIENE dependencias pesadas: $($foundHeavy -join ', ')" -ForegroundColor Red
        Write-Host "   ⚠️  Esto causará que Railway instale todo" -ForegroundColor Red
    }
    
    Write-Host "`n📦 Dependencias en requirements-prod.txt:" -ForegroundColor Cyan
    $prodContent | ForEach-Object { Write-Host "   $_" -ForegroundColor White }
    
} else {
    Write-Host "❌ requirements-prod.txt NO existe" -ForegroundColor Red
}

# Verificar que requirements-ml.txt existe
Write-Host "`n🤖 Verificando requirements-ml.txt..." -ForegroundColor Yellow
if (Test-Path "requirements-ml.txt") {
    $mlContent = Get-Content "requirements-ml.txt"
    Write-Host "✅ requirements-ml.txt existe" -ForegroundColor Green
    Write-Host "📦 Contiene dependencias pesadas:" -ForegroundColor Cyan
    $mlContent | ForEach-Object { Write-Host "   $_" -ForegroundColor White }
} else {
    Write-Host "❌ requirements-ml.txt NO existe" -ForegroundColor Red
}

# Verificar Dockerfile
Write-Host "`n🐳 Verificando Dockerfile..." -ForegroundColor Yellow
if (Test-Path "Dockerfile") {
    $dockerContent = Get-Content "Dockerfile"
    
    # Verificar que solo instala requirements-prod.txt
    if ($dockerContent -match "requirements-prod\.txt") {
        Write-Host "✅ Dockerfile instala requirements-prod.txt" -ForegroundColor Green
    } else {
        Write-Host "❌ Dockerfile NO instala requirements-prod.txt" -ForegroundColor Red
    }
    
    # Verificar que NO instala requirements.txt
    if ($dockerContent -match "requirements\.txt" -and $dockerContent -notmatch "requirements-prod\.txt") {
        Write-Host "❌ Dockerfile instala requirements.txt (PESADO)" -ForegroundColor Red
    } else {
        Write-Host "✅ Dockerfile NO instala requirements.txt" -ForegroundColor Green
    }
    
} else {
    Write-Host "❌ Dockerfile NO existe" -ForegroundColor Red
}

# Verificar .dockerignore
Write-Host "`n🚫 Verificando .dockerignore..." -ForegroundColor Yellow
if (Test-Path ".dockerignore") {
    $ignoreContent = Get-Content ".dockerignore"
    
    if ($ignoreContent -match "requirements-ml\.txt") {
        Write-Host "✅ .dockerignore excluye requirements-ml.txt" -ForegroundColor Green
    } else {
        Write-Host "❌ .dockerignore NO excluye requirements-ml.txt" -ForegroundColor Red
    }
    
    if ($ignoreContent -match "requirements-dev\.txt") {
        Write-Host "✅ .dockerignore excluye requirements-dev.txt" -ForegroundColor Green
    } else {
        Write-Host "❌ .dockerignore NO excluye requirements-dev.txt" -ForegroundColor Red
    }
    
} else {
    Write-Host "❌ .dockerignore NO existe" -ForegroundColor Red
}

# Verificar railway.json
Write-Host "`n🚂 Verificando railway.json..." -ForegroundColor Yellow
if (Test-Path "railway.json") {
    $railwayContent = Get-Content "railway.json" | ConvertFrom-Json
    Write-Host "✅ railway.json existe" -ForegroundColor Green
    
    if ($railwayContent.build.command -match "docker") {
        Write-Host "✅ Usa Docker para build" -ForegroundColor Green
    } else {
        Write-Host "⚠️  NO usa Docker para build" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "❌ railway.json NO existe" -ForegroundColor Red
}

Write-Host "`n🎯 RESUMEN PARA RAILWAY:" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

if ($foundHeavy.Count -eq 0) {
    Write-Host "✅ CONFIGURACIÓN CORRECTA" -ForegroundColor Green
    Write-Host "   Railway instalará SOLO dependencias livianas" -ForegroundColor Green
    Write-Host "   Imagen Docker será < 500MB" -ForegroundColor Green
} else {
    Write-Host "❌ CONFIGURACIÓN INCORRECTA" -ForegroundColor Red
    Write-Host "   Railway instalará dependencias pesadas" -ForegroundColor Red
    Write-Host "   Imagen Docker será > 4GB" -ForegroundColor Red
    Write-Host "   ⚠️  NECESITAS LIMPIAR requirements-prod.txt" -ForegroundColor Red
}

Write-Host "`n📝 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. En Railway: Settings > Deployments > Use Dockerfile = ON" -ForegroundColor White
Write-Host "2. En Railway: Clear cache y redeploy" -ForegroundColor White
Write-Host "3. Verificar que la imagen pesa < 1GB" -ForegroundColor White 