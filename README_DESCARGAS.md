# 📦 Sistema de Descargas - Aegis Code

## 🎯 Descripción

Este sistema permite descargar la aplicación Aegis Code completa para uso local, mientras mantiene la funcionalidad completa en Railway. Los modelos de Machine Learning se descargan dinámicamente solo cuando se necesitan.

## 🚀 Características

### ✅ **Descarga de Aplicación Completa**
- Paquete ZIP con toda la aplicación
- Incluye scripts de instalación automática
- Instrucciones detalladas de instalación
- Configuración lista para desarrollo local

### 🤖 **Descarga Dinámica de Modelos ML**
- **Stanza**: Modelos de procesamiento de lenguaje natural en español
- **NLTK**: Modelos de análisis de texto
- **YARA**: Reglas de detección de malware
- Descarga automática en tiempo de ejecución
- Reutilización de modelos descargados

### 🌐 **Funcionamiento Híbrido**
- **Railway**: Imagen liviana (< 1GB) sin modelos ML
- **Local**: Descarga automática de modelos cuando se necesitan
- **Nube**: Modelos se descargan dinámicamente en el contenedor

## 📋 Requisitos

### Para Uso Local
- Python 3.11 o superior
- pip (gestor de paquetes)
- PowerShell (Windows) o Bash (Linux/Mac)
- Conexión a internet (para descargar modelos ML)

### Para Railway
- Solo dependencias esenciales (requirements-prod.txt)
- Dockerfile optimizado
- Modelos se descargan automáticamente

## 🛠️ Instalación Local

### Opción 1: Instalación Automática (Recomendada)

1. **Descargar desde la aplicación web**
   - Ve a `/downloads/` en la aplicación
   - Haz clic en "Descargar Aplicación Completa"
   - Extrae el archivo ZIP

2. **Ejecutar script de instalación**
   ```powershell
   .\install_local.ps1
   ```

3. **Ejecutar la aplicación**
   ```bash
   python manage.py runserver
   ```

### Opción 2: Instalación Manual

1. **Instalar dependencias**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Configurar base de datos**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Descargar modelos ML**
   ```bash
   python manage.py download_ml_models
   ```

4. **Ejecutar aplicación**
   ```bash
   python manage.py runserver
   ```

## 📁 Estructura del Paquete Descargable

```
aegis_code_local.zip
├── Crud/                    # Aplicación principal
├── Crud_Damian/            # Configuración Django
├── crud_Matias/            # Aplicación adicional
├── manage.py               # Script de gestión Django
├── requirements-dev.txt    # Dependencias de desarrollo
├── install_local.ps1      # Script de instalación automática
├── yara_rules/            # Reglas de detección de malware
├── media/                 # Archivos multimedia
└── INSTRUCCIONES_INSTALACION.txt
```

## 🤖 Gestión de Modelos ML

### Descarga Automática
Los modelos se descargan automáticamente cuando:
- Se ejecuta el análisis de texto por primera vez
- Se accede a funcionalidades que requieren ML
- Se ejecuta el comando de descarga manual

### Descarga Manual
```bash
# Descargar todos los modelos
python manage.py download_ml_models

# Descargar solo Stanza
python manage.py download_ml_models --stanza-only

# Descargar solo NLTK
python manage.py download_ml_models --nltk-only
```

### Verificar Estado
```bash
# Desde la aplicación web
GET /downloads/status/

# Desde Python
from Crud.services import ml_model_manager
status = ml_model_manager.get_models_status()
print(status)
```

## 🔧 Configuración

### Directorios de Modelos
- **Stanza**: `media/ml_models/stanza/`
- **NLTK**: `media/ml_models/nltk_data/`
- **YARA**: `yara_rules/`

### Variables de Entorno
```bash
# Para desarrollo local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Para Railway
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

## 🚀 Despliegue en Railway

### Configuración Optimizada
- **requirements-prod.txt**: Solo dependencias esenciales
- **Dockerfile**: Instalación controlada
- **Descarga dinámica**: Modelos se descargan en tiempo de ejecución

### Ventajas
- ✅ Imagen < 1GB (vs 6.8GB original)
- ✅ Despliegue rápido
- ✅ Funcionalidad completa
- ✅ Modelos actualizados automáticamente

## 🆘 Solución de Problemas

### Error: "Modelos no encontrados"
```bash
# Descargar modelos manualmente
python manage.py download_ml_models

# Verificar directorios
ls media/ml_models/
```

### Error: "Stanza no está instalado"
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

### Error: "Permisos denegados"
```bash
# Ejecutar como administrador (Windows)
# o con sudo (Linux/Mac)
```

### Error: "Conexión a internet"
- Verificar conexión a internet
- Los modelos requieren descarga desde internet
- Tamaño total: ~200MB

## 📊 Estadísticas

### Tamaños de Descarga
- **Aplicación completa**: ~500MB
- **Modelos Stanza**: ~150MB
- **Modelos NLTK**: ~50MB
- **Reglas YARA**: ~1MB

### Tiempos de Descarga
- **Aplicación**: 2-5 minutos (dependiendo de conexión)
- **Modelos ML**: 1-3 minutos (primera vez)
- **Subsecuentes**: Instantáneo (modelos reutilizados)

## 🔄 Actualizaciones

### Actualizar Modelos ML
```bash
# Actualizar todos los modelos
python manage.py download_ml_models --force

# Actualizar solo Stanza
python manage.py download_ml_models --stanza-only --force
```

### Actualizar Aplicación
1. Descargar nueva versión desde `/downloads/`
2. Reemplazar archivos existentes
3. Ejecutar migraciones: `python manage.py migrate`

## 📞 Soporte

### Logs de Descarga
Los logs se guardan en:
- **Django logs**: Configurados en settings.py
- **Consola**: Durante ejecución de comandos
- **Archivos temporales**: `temp_downloads/`

### Comandos Útiles
```bash
# Verificar estado de modelos
python manage.py shell -c "from Crud.services import ml_model_manager; print(ml_model_manager.get_models_status())"

# Limpiar archivos temporales
python manage.py shell -c "from Crud.services import ml_model_manager; ml_model_manager.cleanup_old_models()"

# Verificar espacio en disco
python manage.py shell -c "import shutil; print(f'Espacio libre: {shutil.disk_usage(\".\")[2] / (1024**3):.2f} GB')"
```

## 🎉 ¡Listo!

Una vez instalado, podrás usar Aegis Code localmente con todas las funcionalidades:
- ✅ Escaneo de archivos con YARA
- ✅ Análisis de texto con Stanza
- ✅ Dashboard de seguridad
- ✅ Gestión de empresas
- ✅ Foro de ciberseguridad

¡Disfruta usando Aegis Code en tu entorno local! 🚀 

# Instrucciones para ejecutar scripts descargados en Windows

## 1. Abrir los archivos en un IDE

Los archivos descargados con extensión `.ps1` (PowerShell), `.py` (Python) u otros scripts deben abrirse en un **IDE** (como VS Code, PyCharm, etc.) o en un editor de texto avanzado. Esto es importante porque estos archivos contienen **código** y no deben abrirse como documentos de texto plano o con programas de ofimática.

---

## 2. Permitir la ejecución de scripts en PowerShell

Por seguridad, Windows PowerShell no permite ejecutar scripts por defecto. Si al intentar ejecutar un script ves un error como:

> "File ... cannot be loaded because running scripts is disabled on this system."

Sigue estos pasos para permitir la ejecución **solo en la sesión actual** (recomendado para desarrollo):

### Pasos:

1. **Abre PowerShell como administrador**  
   Haz clic derecho en el icono de PowerShell y selecciona "Ejecutar como administrador".

2. **Ejecuta este comando:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   ```
   Esto permite ejecutar scripts solo en la ventana de PowerShell abierta. Cuando la cierres, la política vuelve a la original.

3. **Ejecuta tu script normalmente:**
   ```powershell
   .\nombre_del_script.ps1
   ```

---

**Nota:** No cambies la política de ejecución global salvo que sepas lo que haces. Si tienes dudas, consulta con el responsable del proyecto.

--- 