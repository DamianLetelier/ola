#!/bin/bash
# Script para limpiar archivos grandes antes del despliegue en Railway

echo "Limpiando archivos grandes para reducir el tamaño del proyecto..."

# Eliminar archivos de base de datos locales
echo "Eliminando archivos de base de datos..."
rm -f db.sqlite3
rm -f *.sqlite3
rm -f *.db

# Eliminar archivos de cache de Python
echo "Eliminando archivos de cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

# Eliminar archivos de media grandes (opcional - solo si no son necesarios)
echo "Eliminando archivos multimedia grandes..."
find media/ -name "*.mp4" -delete 2>/dev/null || true
find media/ -name "*.avi" -delete 2>/dev/null || true
find media/ -name "*.mov" -delete 2>/dev/null || true
find media/ -name "*.gif" -delete 2>/dev/null || true

# Eliminar archivos de presentación grandes
echo "Eliminando archivos de presentación..."
rm -rf "Artefacto-8-Presentación-final/" 2>/dev/null || true

# Eliminar archivos de build
echo "Eliminando archivos de build..."
rm -rf build/ 2>/dev/null || true
rm -rf dist/ 2>/dev/null || true
rm -rf *.egg-info/ 2>/dev/null || true

# Eliminar archivos de logs
echo "Eliminando archivos de logs..."
find . -name "*.log" -delete 2>/dev/null || true

# Eliminar archivos temporales
echo "Eliminando archivos temporales..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true

echo "Limpieza completada. El proyecto está listo para el despliegue."
echo "Tamaño actual del proyecto:"
du -sh . --exclude=.git 