# Script de instalación para Aegis Code Local
# Ejecutar como administrador en PowerShell

Write-Host "=== AEGIS CODE - INSTALACIÓN LOCAL ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python no encontrado. Instala Python 3.11+ desde python.org" -ForegroundColor Red
    exit 1
}

# Verificar pip
Write-Host "Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip no encontrado. Instala pip" -ForegroundColor Red
    exit 1
}

# Actualizar pip
Write-Host "Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependencias
Write-Host "Instalando dependencias de desarrollo..." -ForegroundColor Yellow
if (Test-Path "requirements-dev.txt") {
    pip install -r requirements-dev.txt
    Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "✗ Archivo requirements-dev.txt no encontrado" -ForegroundColor Red
    exit 1
}

# Crear directorios necesarios
Write-Host "Creando directorios necesarios..." -ForegroundColor Yellow
$directories = @(
    "media",
    "media/empresas",
    "media/empleados",
    "media/ml_models",
    "media/ml_models/stanza",
    "media/ml_models/nltk_data",
    "staticfiles"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "✓ Creado: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Existe: $dir" -ForegroundColor Green
    }
}

# Ejecutar migraciones
Write-Host "Ejecutando migraciones de base de datos..." -ForegroundColor Yellow
try {
    python manage.py makemigrations
    python manage.py migrate
    Write-Host "✓ Migraciones completadas" -ForegroundColor Green
} catch {
    Write-Host "✗ Error en migraciones: $_" -ForegroundColor Red
}

# Crear superusuario
Write-Host ""
Write-Host "¿Deseas crear un superusuario? (s/n): " -ForegroundColor Cyan -NoNewline
$createSuper = Read-Host
if ($createSuper -eq "s" -or $createSuper -eq "S") {
    try {
        python manage.py createsuperuser
        Write-Host "✓ Superusuario creado" -ForegroundColor Green
    } catch {
        Write-Host "✗ Error creando superusuario: $_" -ForegroundColor Red
    }
}

# Descargar modelos ML
Write-Host ""
Write-Host "¿Deseas descargar los modelos de ML ahora? (s/n): " -ForegroundColor Cyan -NoNewline
$downloadML = Read-Host
if ($downloadML -eq "s" -or $downloadML -eq "S") {
    Write-Host "Descargando modelos de ML..." -ForegroundColor Yellow
    try {
        python manage.py shell -c "
from Crud.services import ml_model_manager
print('Descargando modelos Stanza...')
ml_model_manager.ensure_stanza_models()
print('Descargando modelos NLTK...')
ml_model_manager.ensure_nltk_models()
print('Modelos descargados exitosamente')
"
        Write-Host "✓ Modelos ML descargados" -ForegroundColor Green
    } catch {
        Write-Host "✗ Error descargando modelos ML: $_" -ForegroundColor Red
    }
}

# Recolectar archivos estáticos
Write-Host "Recolectando archivos estáticos..." -ForegroundColor Yellow
try {
    python manage.py collectstatic --noinput
    Write-Host "✓ Archivos estáticos recolectados" -ForegroundColor Green
} catch {
    Write-Host "✗ Error recolectando archivos estáticos: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== INSTALACIÓN COMPLETADA ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ejecutar la aplicación:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Luego abre: http://127.0.0.1:8000" -ForegroundColor White
Write-Host ""
Write-Host "Para descargar modelos ML más tarde:" -ForegroundColor Yellow
Write-Host "  python manage.py shell -c \"from Crud.services import ml_model_manager; ml_model_manager.ensure_stanza_models(); ml_model_manager.ensure_nltk_models()\"" -ForegroundColor White
Write-Host ""
Write-Host "¡Disfruta usando Aegis Code localmente!" -ForegroundColor Green 