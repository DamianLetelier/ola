# Despliegue en Railway

Este proyecto está configurado para ser desplegado en Railway.

## ⚠️ Importante: Reducción de Tamaño

Railway tiene un límite de 4GB para el procesamiento de imágenes. Para asegurar que tu proyecto se despliegue correctamente, se han implementado las siguientes medidas:

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

### Procfile
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

### 4. Desplegar en Railway
1. Conecta tu repositorio de GitHub a Railway
2. Railway detectará automáticamente que es un proyecto Django
3. Las migraciones se ejecutarán automáticamente
4. Los archivos estáticos se recolectarán automáticamente

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
1. Ejecuta `./clean_for_deploy.sh` para limpiar archivos grandes
2. Verifica que no haya archivos multimedia grandes en el repositorio
3. Asegúrate de que el `.gitignore` esté funcionando correctamente

### Archivos Necesarios Después del Despliegue
- Los archivos de media se pueden subir manualmente después del despliegue
- La base de datos se creará automáticamente en Railway
- Los archivos estáticos se generarán automáticamente 