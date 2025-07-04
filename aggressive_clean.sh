#!/bin/bash
# Script agresivo para limpiar archivos duplicados y innecesarios

echo "=== LIMPIEZA AGRESIVA PARA RAILWAY ==="
echo "Eliminando archivos duplicados y innecesarios..."

# 1. ELIMINAR CARPETAS DUPLICADAS Y INNECESARIAS
echo "1. Eliminando carpetas duplicadas..."

# Eliminar la carpeta de herramientas completa (es una copia duplicada)
echo "   - Eliminando herramientas/ (copia duplicada)"
rm -rf herramientas/ 2>/dev/null || true

# Eliminar carpeta de presentación (contiene archivos grandes)
echo "   - Eliminando Artefacto-8-Presentación-final/ (archivos grandes)"
rm -rf "Artefacto-8-Presentación-final/" 2>/dev/null || true

# Eliminar carpeta de proyecto (parece ser documentación)
echo "   - Eliminando proyecto/ (documentación innecesaria)"
rm -rf proyecto/ 2>/dev/null || true

# 2. ELIMINAR ARCHIVOS DE BASE DE DATOS
echo "2. Eliminando archivos de base de datos..."
rm -f db.sqlite3
rm -f *.sqlite3
rm -f *.db

# 3. ELIMINAR ARCHIVOS MULTIMEDIA GRANDES
echo "3. Eliminando archivos multimedia grandes..."
find . -name "*.mp4" -delete 2>/dev/null || true
find . -name "*.avi" -delete 2>/dev/null || true
find . -name "*.mov" -delete 2>/dev/null || true
find . -name "*.gif" -delete 2>/dev/null || true
find . -name "*.webp" -delete 2>/dev/null || true
find . -name "*.png" -delete 2>/dev/null || true
find . -name "*.jpg" -delete 2>/dev/null || true
find . -name "*.jpeg" -delete 2>/dev/null || true

# 4. ELIMINAR ARCHIVOS DE DOCUMENTOS
echo "4. Eliminando archivos de documentos..."
find . -name "*.docx" -delete 2>/dev/null || true
find . -name "*.doc" -delete 2>/dev/null || true
find . -name "*.pdf" -delete 2>/dev/null || true
find . -name "*.pptx" -delete 2>/dev/null || true
find . -name "*.ppt" -delete 2>/dev/null || true

# 5. ELIMINAR ARCHIVOS DE CACHE Y TEMPORALES
echo "5. Eliminando archivos de cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyd" -delete 2>/dev/null || true

# 6. ELIMINAR ARCHIVOS DE LOGS
echo "6. Eliminando archivos de logs..."
find . -name "*.log" -delete 2>/dev/null || true

# 7. ELIMINAR ARCHIVOS DE BUILD
echo "7. Eliminando archivos de build..."
rm -rf build/ 2>/dev/null || true
rm -rf dist/ 2>/dev/null || true
rm -rf *.egg-info/ 2>/dev/null || true
rm -rf .pytest_cache/ 2>/dev/null || true
rm -rf .coverage 2>/dev/null || true

# 8. ELIMINAR ARCHIVOS DE ENTORNO
echo "8. Eliminando archivos de entorno..."
rm -f environment.yml 2>/dev/null || true
rm -rf .venv/ 2>/dev/null || true
rm -rf venv/ 2>/dev/null || true
rm -rf env/ 2>/dev/null || true

# 9. ELIMINAR ARCHIVOS DE IDE
echo "9. Eliminando archivos de IDE..."
rm -rf .vscode/ 2>/dev/null || true
rm -rf .idea/ 2>/dev/null || true
find . -name "*.sublime-*" -delete 2>/dev/null || true

# 10. ELIMINAR ARCHIVOS DEL SISTEMA
echo "10. Eliminando archivos del sistema..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true

# 11. ELIMINAR CARPETA MEDIA COMPLETA (se recreará en Railway)
echo "11. Eliminando carpeta media/ (se recreará en Railway)..."
rm -rf media/ 2>/dev/null || true

# 12. ELIMINAR ARCHIVOS DE YARA (si no son necesarios para el despliegue)
echo "12. Eliminando archivos de YARA (opcional)..."
rm -rf yara_rules/ 2>/dev/null || true

echo ""
echo "=== LIMPIEZA COMPLETADA ==="
echo "Tamaño actual del proyecto:"
du -sh . --exclude=.git 2>/dev/null || echo "No se pudo calcular el tamaño"

echo ""
echo "Archivos restantes:"
find . -type f -name "*.py" | head -10
echo "..." 