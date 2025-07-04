# Despliegue en Railway

Este proyecto está configurado para ser desplegado en Railway.

## ⚠️ Importante: Dependencias Separadas

Railway tiene un límite de 4GB para el procesamiento de imágenes. El problema principal es que `requirements.txt` incluye librerías de machine learning muy pesadas (PyTorch, Spacy, Stanza, etc.) que no son necesarias para el despliegue web.

### Solución Implementada:
- **`Dockerfile`**: Controla exactamente qué se instala (no más Nixpacks)
- **`requirements-prod.txt`**: Solo dependencias esenciales (~300-600MB)
- **`requirements-dev.txt`**: Todas las dependencias para desarrollo local
- **Railway usará Dockerfile** en lugar de Nixpacks para evitar dependencias innecesarias

### Archivos Excluidos del Repositorio:
- **Carpetas duplicadas**: `herramientas/` (copia completa del proyecto)
- **Archivos de presentación**: `Artefacto-8-Presentación-final/` (14.7MB)
- **Documentación**: `proyecto/` (documentación innecesaria)
- **Archivos multimedia**: `media/` (contiene GIFs de 5.5MB+)
- **Archivos de base de datos**: `db.sqlite3` (6.7MB)
- **Archivos de YARA**: `yara_rules/` (no necesarios para el despliegue)
- **Archivos de entorno**: `environment.yml` (2.5KB)
- **Archivos de cache**: `__pycache__/`, `*.pyc`
- **Archivos de build**: `build/`, `dist/`, `*.egg-info/`
- **Archivos de logs**: `*.log`

## Archivos de Configuración

### Dockerfile
Controla exactamente qué se instala en Railway:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-prod.txt requirements.txt
COPY . .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "Crud_Damian.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### requirements-prod.txt
Solo dependencias esenciales para producción:
```
Django>=5.0
gunicorn
whitenoise
dj-database-url
python-dotenv
django-crispy-forms
crispy-bootstrap5
```

### Procfile (opcional con Dockerfile)
Especifica cómo ejecutar la aplicación:
```
web: gunicorn Crud_Damian.wsgi --log-file -
```

### runtime.txt
Especifica la versión de Python:
```
python-3.11.7
```

### requirements.txt
Incluye todas las dependencias necesarias para producción:
- Django
- Gunicorn (servidor WSGI)
- WhiteNoise (servir archivos estáticos)
- dj-database-url (configuración de base de datos)

## Variables de Entorno

En Railway, configura las siguientes variables de entorno:

1. **SECRET_KEY**: Clave secreta de Django (genera una nueva para producción)
2. **DEBUG**: Establece en 'False' para producción
3. **DATABASE_URL**: URL de la base de datos (Railway la proporciona automáticamente)

## Pasos para Desplegar

### 1. Limpiar el Proyecto (OBLIGATORIO)
Antes de subir a GitHub, ejecuta el script de limpieza agresiva:

**Para Windows PowerShell:**
```powershell
.\aggressive_clean.ps1
```

**Para Linux/Mac:**
```bash
chmod +x aggressive_clean.sh
./aggressive_clean.sh
```

**NOTA**: Este script eliminará archivos duplicados y carpetas innecesarias que no afectan el funcionamiento del programa.

### 2. Verificar el Tamaño
Asegúrate de que el proyecto no exceda 4GB:

**Para Windows PowerShell:**
```powershell
.\check_size.ps1
```

**Para Linux/Mac:**
```bash
chmod +x check_size.sh
./check_size.sh
```

Esto te mostrará qué archivos y carpetas están ocupando más espacio.

### 3. Subir a GitHub
```bash
git add .
git commit -m "Preparado para Railway"
git push origin main
```

### 4. Desplegar en Railway (Dockerfile automático)
1. Conecta tu repositorio de GitHub a Railway
2. **Railway detectará automáticamente el Dockerfile** y lo usará
3. **Nixpacks se desactivará automáticamente** (no más dependencias innecesarias)
4. Railway usará solo las dependencias definidas en `requirements-prod.txt` (~300-600MB)

### 5. Desplegar en Railway
1. Railway detectará automáticamente que es un proyecto Django
2. Las migraciones se ejecutarán automáticamente
3. Los archivos estáticos se recolectarán automáticamente

## Configuraciones Específicas

### Base de Datos
- El proyecto usa `dj-database-url` para configurar la base de datos
- En desarrollo usa SQLite
- En producción usa la base de datos proporcionada por Railway

### Archivos Estáticos
- WhiteNoise se encarga de servir archivos estáticos
- Los archivos se comprimen automáticamente
- Se recolectan en el directorio `staticfiles/`

### Seguridad
- DEBUG se desactiva en producción
- SECRET_KEY se obtiene de variables de entorno
- ALLOWED_HOSTS permite todos los hosts (configurar según necesidad)

## Comandos Útiles

Para desarrollo local:
```bash
python manage.py runserver
```

Para producción (Railway):
```bash
gunicorn Crud_Damian.wsgi
```

## Notas Importantes

- **Tamaño del Proyecto**: Mantén el proyecto por debajo de 4GB para que Railway pueda procesarlo
- **Archivos de Media**: Los archivos de media se excluyen del repositorio para reducir el tamaño
- **Base de Datos**: Railway proporcionará su propia base de datos PostgreSQL
- **Archivos Estáticos**: Se recolectan automáticamente en `staticfiles/`
- **Migraciones**: Se ejecutan automáticamente en Railway
- **Zona Horaria**: El proyecto está configurado para usar la zona horaria de Chile

## Solución de Problemas

### Error: "Image too large"
Si Railway muestra este error:
1. **Asegúrate de usar `requirements-prod.txt`** en Railway (paso 4)
2. Ejecuta `.\aggressive_clean.ps1` para limpiar archivos grandes
3. Verifica que no haya archivos multimedia grandes en el repositorio
4. Asegúrate de que el `.gitignore` esté funcionando correctamente

### Error: "Image too large" o dependencias innecesarias
Si Railway sigue intentando instalar librerías pesadas:
1. **Asegúrate de que el Dockerfile esté en la raíz del proyecto**
2. **Verifica que Nixpacks esté desactivado** (Railway lo hace automáticamente)
3. **El Dockerfile controla exactamente qué se instala**

### Error: "ModuleNotFoundError: No module named 'dj_database_url'"
Este error indica que Railway no está usando el Dockerfile:
1. Verifica que el `Dockerfile` esté en la raíz del proyecto
2. Asegúrate de que Railway detecte el Dockerfile automáticamente
3. No uses `requirements.txt` (contiene librerías pesadas innecesarias)

### Archivos Necesarios Después del Despliegue
- Los archivos de media se pueden subir manualmente después del despliegue
- La base de datos se creará automáticamente en Railway
- Los archivos estáticos se generarán automáticamente 